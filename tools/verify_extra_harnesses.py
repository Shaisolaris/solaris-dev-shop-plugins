#!/usr/bin/env python3
"""Golden source checks and useful local outcomes for additional native profiles."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import build_extra_harness_profiles as builder
from verify_harness_profiles import compare

ROOT = Path(__file__).resolve().parents[1]


def controls(expected):
    with tempfile.TemporaryDirectory(prefix='solaris-extra-controls-') as temp:
        candidate = Path(temp) / 'candidate'
        shutil.copytree(expected, candidate)
        passed = []
        def reject(label):
            try:
                compare(expected, candidate)
            except ValueError:
                passed.append(label)
            else:
                raise ValueError('False acceptance: ' + label)
        entry = candidate / 'index.js'
        original = entry.read_bytes()
        entry.write_text('export default function () {}\n')
        reject('no-op native entrypoint')
        manifest = candidate / 'HARNESS-BUILD.json'
        saved = manifest.read_bytes()
        record = json.loads(saved)
        import hashlib
        record['files']['index.js']['sha256'] = hashlib.sha256(entry.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(record))
        reject('no-op plus edited submitted manifest')
        entry.write_bytes(original)
        manifest.write_bytes(saved)
        index = candidate / 'native/skills.json'
        saved_index = index.read_bytes()
        index.write_text(json.dumps(json.loads(saved_index)[:-1]))
        reject('partial roster')
        index.write_bytes(saved_index)
        entry.chmod(0o755)
        reject('changed executable mode')
        entry.chmod(0o644)
        extra = candidate / 'hooks/hooks.json'
        extra.parent.mkdir()
        extra.write_text('{}')
        reject('undeclared lifecycle hook')
        extra.unlink()
        extra.parent.rmdir()
        entry.unlink()
        entry.symlink_to(expected / 'index.js')
        reject('symlink entrypoint')
        return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['amp', 'cline'], required=True)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    candidate = (args.candidate or ROOT / 'harnesses' / args.host).resolve()
    with tempfile.TemporaryDirectory(prefix='solaris-extra-golden-') as temp:
        expected = Path(temp) / args.host
        builder.build(ROOT, expected, args.host)
        count = compare(expected, candidate)
        assert count == 1974
        index = json.loads((candidate / 'native/skills.json').read_text())
        assert len(index) == len({row['name'] for row in index}) == 62
        package = json.loads((candidate / 'package.json').read_text())
        assert not package.get('scripts') and not package.get('dependencies')
        for row in index:
            result = subprocess.check_output([sys.executable, '-B', str(candidate / 'skills' / row['name'] / 'scripts/run.py'),
                                              '--context'], cwd=temp, text=True, timeout=15)
            assert json.loads(result)['source_commit'] == builder.base.CORE_COMMIT
        result = subprocess.check_output([sys.executable, '-B', str(candidate / 'skills/chief-of-staff/scripts/run.py'),
                                          'intake', 'review this code', '--json'], cwd=temp, text=True, timeout=20)
        assert json.loads(result)['assignment']['primary_capability'] == 'solaris.code-reviewer'
        result = subprocess.check_output([sys.executable, '-B', str(candidate / 'employees/quality-security/security-auditor/provenance_check.py'),
                                          'check', str(candidate), '--exclude', 'examples/capabilities/G38/fixtures', '--json'],
                                         cwd=temp, text=True, timeout=30)
        check = json.loads(result)
        assert check['result'] == 'consistent' and not check['findings']
        report = {'host': args.host, 'exactFilesAndModes': count, 'canonicalFiles': 1199,
                  'actualCallerContexts': 62, 'coordinatorAssignment': 'solaris.code-reviewer',
                  'newCoreCapabilities': 0, 'compositeProvenance': 'consistent',
                  'hostRuntimeAcceptance': 'Separate actual CLI/SDK gate, not implied by this source check'}
        if args.self_test:
            report['rejectedControls'] = controls(expected)
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
