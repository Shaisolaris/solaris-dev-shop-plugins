#!/usr/bin/env python3
"""Build native DSH/Kilo/OpenClaw/Antigravity profiles from an immutable reviewed Solaris payload."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

NATIVE_COMMIT = '085ebb9e9c137c5046c2153b9413d9badd102ce7'
CORE_COMMIT = 'ee38d3de3d4b0d5467a589d5cb908f4964f593fe'
VERSION = '0.63.0'
ROOT = Path(__file__).resolve().parents[1]
OMIT = {'.claude-plugin/plugin.json', 'plugin.json', 'server.mjs', 'native/opencode.mjs'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_files(source):
    archive = subprocess.check_output(['git', '-C', str(source), 'archive', NATIVE_COMMIT, 'copilot/plugin'])
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        for entry in stream:
            if entry.isdir():
                continue
            assert entry.isfile() and entry.name.startswith('copilot/plugin/')
            name = entry.name[len('copilot/plugin/'):]
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
            files[name] = (stream.extractfile(entry).read(), bool(entry.mode & 0o111))
    assert len(files) == 1973
    original = json.loads(files['SOLARIS-BUILD-SOURCE.json'][0])
    assert original['source_commit'] == CORE_COMMIT
    assert not OMIT.intersection(original['canonical_files'])
    return files


def build(source, output, host):
    assert not output.exists(), 'Output must be new; preserve earlier candidates.'
    original = source_files(source)
    omitted = (OMIT | {'package.json'}) if host == 'antigravity' else OMIT
    for name, (data, executable) in original.items():
        if name in omitted:
            continue
        target_name = 'SOURCE-ENTRYPOINT-LAYOUT.json' if name == 'COPILOT-LAYOUT.json' else name
        target = output / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o755 if executable else 0o644)
    package = {
        'name': 'dsh-plugin-solaris-dev-shop' if host == 'deepseek' else ('solaris-dev-shop-' + host),
        'version': VERSION, 'type': 'module', 'license': 'MIT',
        'description': '61 specialist workflows and a chief-of-staff coordinator with local delivery, recovery and evidence tools.',
        'author': {'name': 'Solaris Technologies', 'email': 'shehryar@solaristek.com', 'url': 'https://solaristek.com'},
        'repository': {'type': 'git', 'url': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins.git', 'directory': 'harnesses/' + host},
        'homepage': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins',
        'keywords': ['solaris-dev-shop', 'agent-skills', {'deepseek': 'dsh-plugin', 'kilo': 'kilo', 'openclaw': 'openclaw-plugin', 'antigravity': 'antigravity-plugin'}[host]],
        'main': './native/' + host + '.mjs',
    }
    if host == 'deepseek':
        package['dsh'] = {'bundle': {'patch': './cordis.patch.yml'}}
        package['engines'] = {'dsh': '0.2.1-rc.2'}
        package['exports'] = {'.': './native/deepseek.mjs'}
        (output / 'cordis.patch.yml').write_text('- insert:\n    - id: solaris-dev-shop\n      name: dsh-plugin-solaris-dev-shop\n')
    elif host == 'kilo':
        package['exports'] = {'.': './native/kilo.mjs', './server': './native/kilo.mjs'}
        package['engines'] = {'opencode': '>=7.8.15 <8'}
    if host != 'antigravity':
        (output / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
    if host == 'antigravity':
        (output / 'plugin.json').write_text(json.dumps({'name': 'solaris-dev-shop', 'description': '61 specialist workflows plus a chief-of-staff coordinator, with complete contained Python helpers and resources.'}, indent=2) + '\n')
    elif host == 'openclaw':
        package['openclaw'] = {'extensions': ['./native/openclaw.mjs'], 'compat': {'pluginApi': '>=2026.10.5 <2027'}, 'build': {'openclawVersion': '2026.10.5'}}
        package['main'] = './native/openclaw.mjs'
        (output / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
        (output / 'native/openclaw.mjs').write_bytes((ROOT / 'tools/harness-assets/openclaw.mjs').read_bytes())
        manifest = {'id': 'solaris-dev-shop', 'name': 'Solaris Dev Shop', 'version': VERSION, 'description': package['description'], 'skills': ['./skills'], 'categories': ['developer-tools'], 'configSchema': {'type': 'object', 'additionalProperties': False, 'properties': {}}, 'cliCommands': [{'name': 'solaris', 'description': 'Route a request through the pinned Solaris coordinator', 'hasSubcommands': True}]}
        (output / 'openclaw.plugin.json').write_text(json.dumps(manifest, indent=2) + '\n')
        (output / 'assets/icon.png').write_bytes((output / 'assets/native-plugin-icon.png').read_bytes())
    else:
        (output / 'native' / (host + '.mjs')).write_bytes((ROOT / 'tools/harness-assets' / (host + '.mjs')).read_bytes())
    (output / 'README.md').write_text(
        '# Solaris Dev Shop for ' + {'deepseek': 'DeepSeek Harness', 'kilo': 'Kilo', 'openclaw': 'OpenClaw', 'antigravity': 'Google Antigravity'}[host] + '\n\n'
        '61 specialist employees plus one chief-of-staff coordinator: 62 workflows. '
        'This native profile preserves the reviewed Solaris 0.63.0 runtime and adds zero employee capabilities.\n\n'
        'Install the complete package through the host plugin manager. Host tools, approvals and runtime requirements apply; '
        'Python helpers need Python 3.10 or later. This package grants no permissions, adds no MCP server, changes no model/provider configuration, '
        'and starts no background schedule. The native adapter registers the bundled workflows on demand.\n\n'
        'The canonical source is pinned to ' + CORE_COMMIT + '; the native source is ' + NATIVE_COMMIT + '. '
        'SOLARIS-BUILD-SOURCE.json preserves all 1,196 canonical hashes. HARNESS-BUILD.json binds generated bytes/modes. '
        'Shared runtime and contained resources stay in this complete package; do not install only its skills folder.\n\n'
        'See ../../HARNESS-DISTRIBUTION.md in the source repository for exact install commands, tested host versions, evidence and limits. '
        'MIT licensed. Publisher: Solaris Technologies, https://solaristek.com. Support: https://github.com/Shaisolaris/solaris-dev-shop-plugins/issues.\n'
    )
    canonical = json.loads((output / 'SOLARIS-BUILD-SOURCE.json').read_text())['canonical_files']
    for name, expected in canonical.items():
        assert digest((output / name).read_bytes()) == expected, name
    files = {f.relative_to(output).as_posix(): {'sha256': digest(f.read_bytes()), 'executable': bool(f.stat().st_mode & 0o111)}
             for f in sorted(output.rglob('*')) if f.is_file()}
    record = {'host': host, 'version': VERSION, 'native_source': NATIVE_COMMIT, 'core_source': CORE_COMMIT,
              'canonical_files': len(canonical), 'specialists': 61, 'coordinator': 1,
              'new_employee_capabilities': 0, 'omitted_other_provider_files': sorted(omitted), 'files': files}
    (output / 'HARNESS-BUILD.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    return {'host': host, 'files': len(files) + 1, 'canonical_files': len(canonical)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps([build(args.source, args.output / host, host) for host in ['deepseek', 'kilo', 'openclaw', 'antigravity']]))
