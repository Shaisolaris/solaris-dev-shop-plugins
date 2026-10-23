#!/usr/bin/env python3
"""Rebuild native profiles and reject changed source, adapters, files or modes."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('solaris_harness_builder', ROOT / 'tools/build_harness_profiles.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def inventory(root):
    files = {}
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError('Symlink in native package: ' + name)
        if path.is_file():
            files[name] = (hashlib.sha256(path.read_bytes()).hexdigest(), bool(path.stat().st_mode & 0o111))
    return files


def compare(expected, candidate):
    wanted, found = inventory(expected), inventory(candidate)
    if wanted != found:
        raise ValueError(json.dumps({'missing': sorted(wanted.keys() - found.keys()),
                                    'extra': sorted(found.keys() - wanted.keys()),
                                    'changed': sorted(k for k in wanted.keys() & found.keys() if wanted[k] != found[k])}))
    return len(wanted)


def controls(expected):
    with tempfile.TemporaryDirectory(prefix='solaris-profile-controls-') as temp:
        trial = Path(temp) / 'trial'
        shutil.copytree(expected, trial)
        compare(expected, trial)
        passed = []
        def reject(label):
            try:
                compare(expected, trial)
            except ValueError:
                passed.append(label)
            else:
                raise ValueError('False acceptance of ' + label)
        target = trial / 'native/deepseek.mjs'
        original = target.read_bytes()
        target.write_text("export const name='solaris-dev-shop'; export function apply() {}\n")
        reject('no-op native adapter')
        manifest = trial / 'HARNESS-BUILD.json'
        saved = manifest.read_bytes()
        metadata = json.loads(saved)
        metadata['files']['native/deepseek.mjs']['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(metadata))
        reject('adapter and submitted manifest changed together')
        target.write_bytes(original)
        manifest.write_bytes(saved)
        target.chmod(0o755)
        reject('executable mode changed')
        target.chmod(0o644)
        extra = trial / 'hooks/hooks.json'
        extra.parent.mkdir()
        extra.write_text('{}')
        reject('undeclared automatic hook')
        extra.unlink()
        extra.parent.rmdir()
        target.unlink()
        target.symlink_to(expected / 'native/deepseek.mjs')
        reject('symlink payload')
        target.unlink()
        target.write_bytes(original)
        compare(expected, trial)
        return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    index = json.loads((ROOT / 'copilot/plugin/native/skills.json').read_text())
    kimi = json.loads((ROOT / 'kimi.plugin.json').read_text())
    expected = ['./copilot/plugin/skills/' + row['name'] for row in index]
    assert len(index) == len(set(expected)) == 62 and kimi['skills'] == expected
    assert kimi['name'] == 'solaris-dev-shop' and kimi['version'] == builder.VERSION
    assert set(kimi) <= {'name', 'version', 'description', 'author', 'homepage', 'license', 'skills', 'interface'}
    pi = json.loads((ROOT / 'package.json').read_text())
    assert pi['pi']['skills'] == [path + '/SKILL.md' for path in expected]
    assert set(pi['pi']) <= {'skills', 'extensions', 'prompts', 'themes'}
    assert not any(pi['pi'].get(key) for key in ['extensions', 'prompts', 'themes'])
    assert not pi.get('scripts') and not pi.get('dependencies')
    for path in expected:
        assert (ROOT / path / 'SKILL.md').is_file() and (ROOT / path / 'scripts/run.py').is_file()
    reports = []
    with tempfile.TemporaryDirectory(prefix='solaris-harness-rebuild-') as temp:
        for host in ['deepseek', 'kilo', 'openclaw', 'antigravity']:
            expected = Path(temp) / host
            builder.build(ROOT, expected, host)
            candidate = ROOT / 'harnesses' / host
            count = compare(expected, candidate)
            entries = sorted(candidate.glob('skills/*/scripts/run.py'))
            assert len(entries) == 62
            for entry in entries:
                result = json.loads(subprocess.check_output([sys.executable, '-B', str(entry), '--context'], cwd=temp, text=True))
                assert result['source_commit'] == builder.CORE_COMMIT
            caller = subprocess.check_output([sys.executable, '-B', str(candidate / 'skills/chief-of-staff/scripts/run.py'),
                                              'intake', 'review this code', '--json'], cwd=temp, text=True)
            assert json.loads(caller)['assignment']['primary_capability'] == 'solaris.code-reviewer'
            report = {'host': host, 'exact_files_and_modes': count, 'canonical_files': 1199,
                      'native_contexts': len(entries), 'actual_assignment': 'solaris.code-reviewer'}
            if host == 'deepseek' and args.self_test:
                report['rejected_controls'] = controls(expected)
            reports.append(report)
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
