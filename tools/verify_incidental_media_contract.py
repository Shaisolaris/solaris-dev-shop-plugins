#!/usr/bin/env python3
"""Read original vendor reports and test the exact native media-applicability guard."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import tempfile

SPEC = importlib.util.spec_from_file_location('media_contract', Path(__file__).with_name('validate_incidental_media.py'))
MEDIA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MEDIA)


def verify(evidence):
    manifest = json.loads((evidence / 'partition.json').read_text())
    validated = {}
    reports = {}
    for scope in manifest['scopes']:
        directory = evidence / 'scopes' / scope['id']
        report = json.loads((directory / 'raw-report.json').read_text())
        if report['analysis_completeness']['scope_exclusions']:
            images = MEDIA.native_media_contract(report, directory / 'input', scope['files'])
            validated.update(images)
            reports[scope['id']] = (report, directory / 'input', scope['files'])
    if len(validated) != 8 or validated['assets/demo.gif']['framesDecoded'] != 33:
        raise ValueError('Expected the unchanged seven PNGs and 33-frame GIF')
    passed = []
    with tempfile.TemporaryDirectory(prefix='solaris-media-negative-') as name:
        temporary = Path(name)
        first_root = reports['scope-000'][1]
        for suffix, source in (('.png', first_root / 'assets/icon.png'), ('.gif', first_root / 'assets/demo.gif')):
            target = temporary / ('trailing' + suffix)
            target.write_bytes(source.read_bytes() + b'PRIVATE-TRAILING-CONTROL')
            try:
                MEDIA.validate_image(target)
            except ValueError:
                passed.append('trailing-bytes-' + suffix)
            else:
                raise ValueError('Trailing bytes were accepted')
        target = temporary / 'not-an-image.png'
        target.write_bytes(b'MZ-private-inert-format-control')
        try:
            MEDIA.validate_image(target)
        except ValueError:
            passed.append('misleading-image-suffix')
        else:
            raise ValueError('An executable signature qualified as an image')
        executable = temporary / 'executable.png'
        executable.write_bytes((first_root / 'assets/icon.png').read_bytes())
        executable.chmod(0o700)
        try:
            MEDIA.validate_image(executable)
        except ValueError:
            passed.append('executable-image-mode')
        else:
            raise ValueError('An executable-mode image qualified')
        link = temporary / 'link.png'
        link.symlink_to(first_root / 'assets/icon.png')
        try:
            MEDIA.validate_image(link)
        except ValueError:
            passed.append('symlink-image')
        else:
            raise ValueError('A symlink qualified')
    report, root, files = reports['scope-000']
    mutations = {
        'native-partial-stays-blocked': lambda doc: doc['analysis_completeness'].update(is_complete=False),
        'real-ledger-gap-stays-blocked': lambda doc: doc['analysis_completeness']['ledger_exceptions'].append(
            {'outcome': 'partial', 'reason_code': 'runtime_limit', 'path': 'assets/icon.png'}),
        'explicit-source-exclusion-stays-blocked': lambda doc: doc['analysis_completeness']['scope_exclusions'][0].update(
            reason_code='explicit_exclusion'),
        'missing-binary-yara-stays-blocked': lambda doc: next(
            item for item in doc['analysis_completeness']['analyzer_statuses']
            if item['analyzer_id'] == 'static_yara').update(completed=149),
    }
    for label, mutate in mutations.items():
        changed = copy.deepcopy(report)
        mutate(changed)
        try:
            MEDIA.native_media_contract(changed, root, files)
        except ValueError:
            passed.append(label)
        else:
            raise ValueError('A genuine failure was accepted: ' + label)
    return {'vendorPolicy': 'Stock 2.13.2 docs/scan-completeness.md incidental-media rows; no partial status is overridden.',
            'nativeCompleteReportsOnly': True, 'vendorReportBytesChanged': False,
            'images': validated, 'mediaNegativeControlsPassed': passed,
            'nvidiaSourceChanged': False, 'wholePluginCleared': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scopes', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.scopes), indent=2))
