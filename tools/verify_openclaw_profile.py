#!/usr/bin/env python3
"""Verify the OpenClaw candidate against immutable source and a golden rebuild."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CORE = 'ab0061f2b67abecbcb2921371da668a18dc7d64a'
EXPECTED_NATIVE = 'e02d8002d195f929e30fb5063bd04d4ed27190d6'
EXPECTED_PACKAGER = '129781961be54cc2f12d6bafe80e81d6a1cd8d02'
spec = importlib.util.spec_from_file_location('openclaw_builder', ROOT / 'tools/build_openclaw_profile.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def compare(expected, candidate):
    if builder.inventory(expected) != builder.inventory(candidate):
        raise ValueError('Candidate differs from the immutable-input golden build')


def canonical_checks(candidate, baseline):
    original = json.loads((baseline / 'SOLARIS-BUILD-SOURCE.json').read_text())
    actual = json.loads((candidate / 'SOLARIS-BUILD-SOURCE.json').read_text())
    relocated = lambda name: 'source-config/' + name if name.startswith('.github/') else name
    expected = {relocated(name): digest for name, digest in original['canonical_files'].items()}
    mapping = dict(original['source_path_map'])
    mapping.update({name: relocated(name) for name in original['canonical_files'] if name.startswith('.github/')})
    if actual['source_commit'] != EXPECTED_CORE or actual['canonical_files'] != expected or actual['source_path_map'] != mapping:
        raise ValueError('Canonical source inventory/provenance differs from trusted source')
    if len(expected) != 1200:
        raise ValueError('Unexpected canonical inventory size')
    for name, digest in expected.items():
        source_name = name.removeprefix('source-config/') if name.startswith('source-config/.github/') else name
        path = candidate / name
        if path.is_symlink() or not path.is_file() or builder.sha(path.read_bytes()) != digest:
            raise ValueError('Missing/changed canonical source: ' + name)
        if bool(path.stat().st_mode & 0o111) != bool((baseline / source_name).stat().st_mode & 0o111):
            raise ValueError('Changed canonical executable mode: ' + name)


def controls(expected):
    with tempfile.TemporaryDirectory(prefix='openclaw-candidate-controls-') as temporary:
        trial = Path(temporary) / 'trial'
        shutil.copytree(expected, trial)
        cases = []
        def reject(label, mutate):
            mutate()
            try:
                compare(expected, trial)
            except (ValueError, OSError):
                cases.append(label)
            else:
                raise ValueError('False acceptance: ' + label)
            shutil.rmtree(trial)
            shutil.copytree(expected, trial)
        helper = 'employees/engineering/devops-engineer/local_deploy.py'
        reject('changed canonical helper', lambda: (trial / helper).write_text('raise SystemExit(0)\n'))
        reject('missing refusal fixture', lambda: (trial / 'examples/capabilities/G25/fixtures/malformed-events.jsonl').unlink())
        reject('missing workflow', lambda: (trial / 'skills/security-auditor/SKILL.md').unlink())
        reject('no-op native adapter', lambda: (trial / 'native/openclaw.mjs').write_text('export default {};\n'))
        def forged():
            target = trial / helper
            target.write_text('raise SystemExit(0)\n')
            for filename, field in [('SOLARIS-BUILD-SOURCE.json', 'canonical_files'), ('HARNESS-BUILD.json', 'files')]:
                path = trial / filename
                record = json.loads(path.read_text())
                if field == 'files':
                    record[field][helper]['sha256'] = builder.sha(target.read_bytes())
                else:
                    record[field][helper] = builder.sha(target.read_bytes())
                path.write_text(json.dumps(record))
        reject('changed helper plus both supplied manifests', forged)
        def lifecycle():
            path = trial / 'package.json'
            record = json.loads(path.read_text())
            record['scripts'] = {'postinstall': 'echo synthetic-control'}
            path.write_text(json.dumps(record))
        reject('added install lifecycle', lifecycle)
        def hook():
            path = trial / 'hooks/hooks.json'
            path.parent.mkdir()
            path.write_text('{}')
        reject('undeclared automatic hook', hook)
        reject('changed entrypoint mode', lambda: (trial / 'skills/chief-of-staff/scripts/run.py').chmod(
            (trial / 'skills/chief-of-staff/scripts/run.py').stat().st_mode ^ 0o111))
        def symlink():
            path = trial / helper
            path.unlink()
            path.symlink_to(expected / helper)
        reject('symlink payload', symlink)
        reject('removed canonical license', lambda: (trial / 'LICENSE').unlink())
        compare(expected, trial)
        return cases


def verify(source, packager, candidate, self_test=False):
    if (builder.CORE, builder.NATIVE, builder.PACKAGER, builder.VERSION) != (
            EXPECTED_CORE, EXPECTED_NATIVE, EXPECTED_PACKAGER, '0.67.0'):
        raise ValueError('Unexpected build input or version pins')
    with tempfile.TemporaryDirectory(prefix='openclaw-golden-') as temporary:
        temporary = Path(temporary)
        expected = temporary / 'expected'
        builder.build(source, packager, ROOT, expected)
        # Reconstruct the independent canonical inventory from the original
        # reviewed packager, rather than trusting either supplied manifest.
        spec = importlib.util.spec_from_file_location('canonical_packager', Path(packager) / 'tools/build_native_plugins.py')
        original = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(original)
        original.git = lambda *args: builder.git(source, *args)
        original.build(EXPECTED_CORE, temporary / 'canonical')
        canonical_checks(candidate, temporary / 'canonical/plugin')
        compare(expected, candidate)
        index = json.loads((candidate / 'native/skills.json').read_text())
        if len(index) != 62:
            raise ValueError('Expected all 62 workflows')
        for row in index:
            entry = candidate / 'skills' / row['name'] / 'scripts/run.py'
            output = subprocess.check_output([sys.executable, '-B', str(entry), '--context'], cwd=temporary, text=True)
            if json.loads(output)['source_commit'] != EXPECTED_CORE:
                raise ValueError('Caller is not bound to current source: ' + row['name'])
        output = subprocess.check_output([sys.executable, '-B', str(candidate / 'skills/chief-of-staff/scripts/run.py'),
                                         'intake', 'review this code', '--json'], cwd=temporary, text=True)
        assignment = json.loads(output)
        if assignment['assignment']['primary_capability'] != 'solaris.code-reviewer' or assignment['performed_work'] is not False:
            raise ValueError('Fresh native caller did not return the bounded assignment')
        result = {'result': 'PASS', 'version': '0.67.0', 'core': EXPECTED_CORE,
                  'files': len(builder.inventory(candidate)), 'canonical_files': 1200, 'fresh_callers': 62,
                  'assignment': 'solaris.code-reviewer', 'provider_admission': False}
        if self_test:
            result['rejected_controls'] = controls(expected)
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--packager', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, default=ROOT / 'harnesses/openclaw')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.source.resolve(), args.packager.resolve(), args.candidate.resolve(), args.self_test), indent=2))
