#!/usr/bin/env python3
"""Install the actual Cline plugin and verify native discovery, worker tools and bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', required=True, type=Path)
    parser.add_argument('--modules', required=True, type=Path)
    parser.add_argument('--candidate', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--git-source')
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    workspace = work / 'workspace'
    workspace.mkdir()
    env = {key: os.environ[key] for key in ['HOME', 'PATH', 'TMPDIR', 'TEMP', 'TMP', 'SYSTEMROOT', 'SSL_CERT_FILE']
           if key in os.environ}
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
    for kind in ['config', 'data', 'cache', 'state']:
        directory = work / kind
        directory.mkdir()
        env['XDG_' + kind.upper() + '_HOME'] = str(directory)
    npmrc = work / 'empty.npmrc'
    npmrc.touch()
    env.update({'CLINE_DIR': str(work / 'cline-config'), 'CLINE_DATA_DIR': str(work / 'cline-data'),
                'DO_NOT_TRACK': '1', 'npm_config_userconfig': str(npmrc), 'npm_config_cache': str(work / 'npm-cache'),
                'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'credential.helper', 'GIT_CONFIG_VALUE_0': '',
                'GIT_TERMINAL_PROMPT': '0'})
    cli = str(args.cli.resolve())
    version = subprocess.check_output([cli, '--version'], cwd=workspace, env=env, text=True).strip()
    assert version == '3.0.73', version
    source = args.git_source or str(args.candidate.resolve())
    install = subprocess.run([cli, 'plugin', 'install', source, '--cwd', str(workspace), '--json'], cwd=workspace,
                             env=env, text=True, capture_output=True, timeout=180)
    (work / 'install.stdout').write_text(install.stdout)
    (work / 'install.stderr').write_text(install.stderr)
    install.check_returncode()
    result = json.loads(install.stdout)
    assert not result['mcpSyncFailures'] and len(result['entryPaths']) == 1, result
    entry = Path(result['entryPaths'][0])
    installed = entry.parent
    assert installed.is_relative_to(work) and not installed.is_symlink(), installed
    assert not any(path.is_symlink() for path in installed.rglob('*')), 'Symlink in installed profile'
    retained_git = (installed / '.git').exists()
    if retained_git:
        pinned = re.fullmatch(r'(https://github.com/Shaisolaris/solaris-dev-shop-cline\.git)@([0-9a-f]{40})', source)
        assert pinned and (installed / '.git').is_dir(), 'Unexpected clone metadata'
        # This manager retains its clone. Bind it to the requested public commit;
        # never remove metadata or confuse it with distributed product files.
        revision = subprocess.check_output(['git', '-C', str(installed), 'rev-parse', 'HEAD'],
                                           env=env, text=True, timeout=15).strip()
        remote = subprocess.check_output(['git', '-C', str(installed), 'config', '--get', 'remote.origin.url'],
                                         env=env, text=True, timeout=15).strip()
        assert revision == pinned[2] and remote.rstrip('/') == pinned[1], 'Clone identity differs from requested source'
        hooks = installed / '.git/hooks'
        assert not hooks.exists() or all(path.is_file() and path.name.endswith('.sample') for path in hooks.iterdir()), 'Unexpected active Git hook'
    expected_files = {path.relative_to(args.candidate).as_posix(): path
                      for path in args.candidate.rglob('*') if path.is_file()}
    actual_files = {path.relative_to(installed).as_posix(): path
                    for path in installed.rglob('*') if path.is_file() and '.git' not in path.relative_to(installed).parts}
    assert set(actual_files) == set(expected_files), (set(actual_files) - set(expected_files), set(expected_files) - set(actual_files))
    byte_identical = 0
    for name, original in expected_files.items():
        actual = actual_files[name]
        assert not actual.is_symlink() and bool(actual.stat().st_mode & 0o111) == bool(original.stat().st_mode & 0o111), name
        if actual.read_bytes() == original.read_bytes():
            byte_identical += 1
            continue
        # The first-party installer removes only host-provided optional SDK declarations.
        assert name == 'package.json', name
        manifest = json.loads(original.read_text())
        assert manifest.pop('peerDependencies') == {'@cline/sdk': '>=0.0.95 <0.1'}
        assert manifest.pop('peerDependenciesMeta') == {'@cline/sdk': {'optional': True}}
        assert json.loads(actual.read_text()) == manifest, 'Unexpected installed package transformation'
    assert len(actual_files) == 1974 and byte_identical in {1973, 1974}
    provenance = json.loads((installed / 'SOLARIS-BUILD-SOURCE.json').read_text())
    assert len(provenance['canonical_files']) == 1197
    for name, digest in provenance['canonical_files'].items():
        mapped = provenance.get('source_path_map', {}).get(name, name)
        assert hashlib.sha256((installed / mapped).read_bytes()).hexdigest() == digest, name
    index = json.loads((installed / 'native/skills.json').read_text())
    assert len(index) == len({row['name'] for row in index}) == 62
    for row in index:
        context = subprocess.check_output([sys.executable, '-B', str(installed / 'skills' / row['name'] / 'scripts/run.py'),
                                           '--context'], cwd=workspace, env=env, text=True, timeout=15)
        assert json.loads(context)['source_commit'] == '3a577e42c48473f6ef8680950dd55c067820d5d3'
    for section in ['skills', 'tools']:
        result = subprocess.run([cli, 'config', section, '--json'], cwd=workspace, env=env,
                                capture_output=True, text=True, check=True, timeout=45)
        (work / (section + '.json')).write_text(result.stdout)
    tools = json.loads((work / 'tools.json').read_text())
    own = [tool for tool in tools if tool.get('name') == 'solaris_intake']
    assert len(own) == 1 and own[0]['enabled'] and own[0]['path'] == str(entry), own
    verifier = Path(__file__).with_name('verify_cline_sdk.mjs')
    result = subprocess.run(['node', str(verifier), str(args.modules.resolve()), str(entry), str(work / 'skills.json'), str(workspace)],
                            cwd=workspace, env=env, capture_output=True, text=True, timeout=90)
    (work / 'sdk.stdout').write_text(result.stdout)
    (work / 'sdk.stderr').write_text(result.stderr)
    result.check_returncode()
    sdk = json.loads(result.stdout)
    check = subprocess.check_output([sys.executable, '-B', str(installed / 'employees/quality-security/security-auditor/provenance_check.py'),
                                     'check', str(installed), '--exclude', 'examples/capabilities/G38/fixtures', '--json'],
                                    cwd=workspace, env=env, text=True, timeout=30)
    provenance_check = json.loads(check)
    assert provenance_check['result'] == 'consistent' and not provenance_check['findings']
    print(json.dumps({'host': 'Cline ' + version, 'profileFiles': len(actual_files), 'byteIdenticalFiles': byte_identical,
                      'retainedGitMetadata': 'Requested exact public commit verified; sample hooks only' if retained_git else None,
                      'permittedInstallerNormalization': 'Only removal of two optional host SDK dependency fields, if present',
                      'allExecutableModesMatch': True, 'canonicalHashes': 1197, 'actualCallerContexts': 62,
                      'compositeProvenance': 'consistent', 'sdk': sdk, 'pass': True}, indent=2))


if __name__ == '__main__':
    main()
