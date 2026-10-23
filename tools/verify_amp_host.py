#!/usr/bin/env python3
"""Check the real Amp plugin process without a model, account, or owner profile."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from verify_harness_profiles import compare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', required=True, type=Path)
    parser.add_argument('--candidate', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    env = {key: os.environ[key] for key in ['HOME', 'PATH', 'TMPDIR', 'TEMP', 'TMP', 'SYSTEMROOT', 'SSL_CERT_FILE']
           if key in os.environ}
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
    for kind in ['config', 'data', 'cache', 'state']:
        directory = work / kind
        directory.mkdir()
        env['XDG_' + kind.upper() + '_HOME'] = str(directory)
    settings = work / 'config/amp/settings.json'
    settings.parent.mkdir()
    settings.write_text(json.dumps({'amp.skills.disableClaudeCodeSkills': True,
                                    'amp.skills.disableGlobalAgentsSkills': True}))
    env['DO_NOT_TRACK'] = '1'
    cli = str(args.cli.resolve())
    version = subprocess.check_output([cli, '--version'], cwd=work, env=env, text=True, timeout=15).strip().split()[0]
    assert version == '0.0.1792680614-g8973a3', version
    installed = work / 'config/amp/plugins/solaris-dev-shop'
    shutil.copytree(candidate, installed)
    assert compare(candidate, installed) == 1977

    # The published directory remains byte-exact. A separate disposable copy
    # forwards registration to the real API and calls its registered callback.
    probe = work / 'native-callback-probe'
    shutil.copytree(installed, probe)
    (probe / 'index.js').rename(probe / 'reviewed-entry.js')
    shutil.copyfile(Path(__file__).with_name('amp_host_probe.mjs'), probe / 'index.js')
    process = subprocess.run([cli, 'plugins', 'exec', str(probe), 'tool.result', '--data', '{}'],
                             cwd=work, env=env, text=True, capture_output=True, timeout=90)
    (work / 'native.stdout').write_text(process.stdout)
    (work / 'native.stderr').write_text(process.stderr)
    process.check_returncode()
    report = json.loads((probe / 'HOST-CALLBACK-PASS.json').read_text())
    assert report['pass'] and report['registeredSkillCalls'] == 62
    assert report['invalidInputControls'] == 3 and report['modelCalls'] == 0
    assert compare(candidate, installed) == 1977
    print(json.dumps({'host': 'Amp ' + version, 'profileFilesAndModes': 1977,
                      'nativeCallback': report, 'ownerProfileModified': False,
                      'authenticatedDiscovery': 'Separate stock CLI gate; not implied by this unauthenticated worker check',
                      'pass': True}, indent=2))


if __name__ == '__main__':
    main()
