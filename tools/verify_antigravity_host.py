#!/usr/bin/env python3
"""Run the official pinned plugin manager only in a fresh hosted Linux CI home."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    assert sys.platform == 'linux' and platform.machine() == 'x86_64', 'Requires Linux x86_64'
    assert os.environ.get('GITHUB_ACTIONS') == 'true', 'Run this check on a fresh hosted runner'
    assert os.environ.get('RUNNER_ENVIRONMENT') == 'github-hosted', 'No owner/self-hosted profile'
    google_home = Path.home() / '.gemini'
    assert not google_home.exists(), 'Refuse access to an existing Google profile'
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    pin = json.loads((ROOT / 'tools/native-hosts/antigravity-linux.json').read_text())
    assert pin['url'].startswith('https://storage.googleapis.com/antigravity-public/')
    with urllib.request.urlopen(pin['url'], timeout=120) as response:
        payload = response.read(200 * 1024 * 1024 + 1)
    assert len(payload) <= 200 * 1024 * 1024
    assert hashlib.sha512(payload).hexdigest() == pin['sha512'], 'Official binary digest mismatch'
    with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
        entry = archive.getmember('antigravity')
        assert entry.isfile(), 'Expected one regular native executable'
        binary = work / 'agy'
        binary.write_bytes(archive.extractfile(entry).read())
        binary.chmod(0o755)
    env = {key: value for key, value in os.environ.items()
           if not re.search(r'(^|_)(API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIALS)($|_)', key)
           and key != 'SSH_AUTH_SOCK'}
    env['AGY_CLI_DISABLE_AUTO_UPDATE'] = 'true'
    env['DO_NOT_TRACK'] = '1'
    profile = ROOT / 'harnesses/antigravity'

    def run(label, *command):
        result = subprocess.run([str(binary), *command], cwd=work, env=env,
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
        (work / (label + '.stdout')).write_text(result.stdout)
        (work / (label + '.stderr')).write_text(result.stderr)
        assert result.returncode == 0, (label, result.returncode, result.stdout[-2000:], result.stderr[-2000:])
        return result.stdout

    run('install', 'plugin', 'install', str(profile))
    catalog = json.loads(run('list', 'plugin', 'list', '--json'))
    rows = catalog if isinstance(catalog, list) else catalog['plugins']
    own = [row for row in rows if row['name'] == 'solaris-dev-shop']
    assert len(own) == 1, 'Native plugin entry absent or duplicated'
    row = own[0]
    assert row.get('enabled') is True and len(row['skills']) == 62, row
    installed = Path(row['path']).resolve()
    assert installed.is_relative_to(google_home.resolve()) and installed != profile.resolve()
    count = 0
    for source in profile.rglob('*'):
        assert not source.is_symlink()
        if not source.is_file():
            continue
        target = installed / source.relative_to(profile)
        assert target.is_file() and not target.is_symlink() and target.read_bytes() == source.read_bytes(), str(source)
        assert bool(target.stat().st_mode & 0o111) == bool(source.stat().st_mode & 0o111), str(source)
        count += 1
    index = json.loads((installed / 'native/skills.json').read_text())
    for skill in index:
        result = subprocess.run([sys.executable, '-B', str(installed / 'skills' / skill['name'] / 'scripts/run.py'), '--context'],
                                cwd=work, env=env, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, (skill['name'], result.stderr)
        assert json.loads(result.stdout)['source_commit'] == 'ee38d3de3d4b0d5467a589d5cb908f4964f593fe'
    result = subprocess.run([sys.executable, '-B', str(installed / 'skills/chief-of-staff/scripts/run.py'),
                             'intake', 'review this code', '--json'], cwd=work, env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assignment = json.loads(result.stdout)
    assert assignment['assignment']['primary_capability'] == 'solaris.code-reviewer' and assignment['performed_work'] is False
    report = {'pass': True, 'host': 'Antigravity CLI', 'version': pin['version'], 'sha512': pin['sha512'],
              'nativeWorkflows': len(row['skills']), 'installedFilesAndModes': count, 'liveContexts': len(index),
              'coordinatorAssignment': 'solaris.code-reviewer', 'modelCalls': 0,
              'ownerProfileAccess': False, 'providerApproval': False}
    (work / 'PASS.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
