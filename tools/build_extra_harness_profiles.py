#!/usr/bin/env python3
"""Build Amp/Cline native plugins around the unchanged reviewed contained payload."""
import argparse
import hashlib
import json
from pathlib import Path
import build_harness_profiles as base

ROOT = Path(__file__).resolve().parents[1]


def build(source, output, host):
    if host not in {'amp', 'cline'}:
        raise ValueError('Unknown additional native host')
    base.build(source, output, 'kilo')
    (output / 'native/kilo.mjs').unlink()
    (output / 'index.js').write_bytes((ROOT / 'tools/harness-assets' / (host + '.js')).read_bytes())
    (output / 'native/intake.mjs').write_bytes((ROOT / 'tools/harness-assets/intake.mjs').read_bytes())
    package = {
        'name': 'solaris-dev-shop-' + host, 'version': base.VERSION, 'type': 'module',
        'license': 'MIT', 'main': './index.js',
        'description': '61 Solaris specialist workflows and a chief-of-staff coordinator with contained local tools.',
        'author': {'name': 'Solaris Technologies', 'email': 'shehryar@solaristek.com', 'url': 'https://solaristek.com'},
        'homepage': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins',
        'repository': {'type': 'git', 'url': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins.git',
                       'directory': 'harnesses/' + host},
    }
    if host == 'cline':
        package.update({'cline': {'plugins': [{'paths': ['./index.js'], 'capabilities': ['tools']}]},
                        'peerDependencies': {'@cline/sdk': '>=0.0.95 <0.1'},
                        'peerDependenciesMeta': {'@cline/sdk': {'optional': True}}})
    (output / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
    (output / 'README.md').write_text(
        '# Solaris Dev Shop for ' + ('Amp' if host == 'amp' else 'Cline') + '\n\n'
        '61 specialists plus a chief-of-staff coordinator: 62 workflows. Complete reviewed source and local helpers are retained; '
        'this distribution adds zero core employee capabilities. Install the complete directory plugin, not its skills alone.\n\n'
        + ('The native Amp directory entry registers each exact bundled skill through registerSkill, with host-owned namespacing. '
           if host == 'amp' else 'The Cline package manifest declares its SDK entrypoint; Cline discovers the top-level bundled skills. ') +
        'A real solaris_intake tool routes a request through the pinned Python coordinator and returns an assignment. '
        'It does not run specialist work. It accepts one nonempty UTF-8 request up to 32KiB, uses execFile with no shell, '
        'a 20second timeout and a minimal child environment. No lifecycle hooks, model/provider changes, grants, MCP, network calls or background jobs.\n\n'
        'Local helpers need Python3.10+ and PyYAML on the host PATH. Individual specialists retain their documented prerequisites and permissions. '
        'Amp hosted/Puck and Cline VS Code/JetBrains support are separate client gates, not established by native CLI/SDK discovery.\n\n'
        'Source: core ' + base.CORE_COMMIT + ', reviewed native ' + base.NATIVE_COMMIT + '. '
        'SOLARIS-BUILD-SOURCE.json preserves1199 canonical hashes; HARNESS-BUILD.json records every profile byte/mode. '
        'See ../../HARNESS-DISTRIBUTION.md in the source repository for actual tested revisions, installation and publication status. '
        'A prepared profile alone does not establish a passing native install or vendor approval.\n\n'
        'MIT licensed. Solaris Technologies, https://solaristek.com. Support: https://github.com/Shaisolaris/solaris-dev-shop-plugins/issues.\n')
    record = json.loads((output / 'HARNESS-BUILD.json').read_text())
    record.update({'host': host, 'base_contained_profile': 'kilo', 'native_registration': host + ' directory/package plugin'})
    record['files'] = {path.relative_to(output).as_posix(): {
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'executable': bool(path.stat().st_mode & 0o111)}
        for path in sorted(output.rglob('*')) if path.is_file() and path != output / 'HARNESS-BUILD.json'}
    (output / 'HARNESS-BUILD.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    return {'host': host, 'files': len(record['files']) + 1, 'canonical_files': 1200}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps([build(args.source, args.output / host, host) for host in ['amp', 'cline']]))
