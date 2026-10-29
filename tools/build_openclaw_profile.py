#!/usr/bin/env python3
"""Build the complete OpenClaw security candidate without Copilot resource aliases.

Canonical source and the existing guarded native entrypoints are immutable inputs.
No code is installed, registered, submitted or published by this builder.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

CORE = '5efe9a59ac1b87e88010e4c97518e8bc8d1267eb'
PACKAGER = '129781961be54cc2f12d6bafe80e81d6a1cd8d02'
NATIVE = 'd3f6febc027631a987ff84795f24a9cb40b7e7d2'
VERSION = '0.70.0'
OMIT = {'.claude-plugin/plugin.json', 'plugin.json', 'server.mjs', 'native/opencode.mjs'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def pinned_file(repo, revision, name):
    row = git(repo, 'ls-tree', revision, '--', name).decode().strip()
    if not row or row.split()[0] not in {'100644', '100755'}:
        raise ValueError('Missing/non-regular pinned input: ' + name)
    return git(repo, 'show', revision + ':' + name), row.split()[0] == '100755'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in package: ' + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = {
                'sha256': sha(path.read_bytes()), 'executable': bool(path.stat().st_mode & 0o111)}
    return result


def build(source, packager, native_source, output):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('Use a new output directory; preserve earlier candidates')
    if git(source, 'rev-parse', 'HEAD').decode().strip() != CORE:
        raise ValueError('Source checkout must be at the exact reviewed candidate')
    for name in ['tools/build_native_plugins.py', 'tools/native-plugin-assets/icon.png',
                 'tools/native-plugin-assets/DATA-HANDLING.md']:
        data, _ = pinned_file(packager, PACKAGER, name)
        if (Path(packager) / name).is_symlink() or (Path(packager) / name).read_bytes() != data:
            raise ValueError('Changed reviewed packager input: ' + name)
    spec = importlib.util.spec_from_file_location('reviewed_solaris_packager',
                                                Path(packager) / 'tools/build_native_plugins.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.git = lambda *args: git(source, *args)
    with tempfile.TemporaryDirectory(prefix='solaris-openclaw-build-') as temporary:
        temporary = Path(temporary)
        module.build(CORE, temporary / 'base')
        base = temporary / 'base/plugin'
        original = json.loads((base / 'SOLARIS-BUILD-SOURCE.json').read_text())
        if len(original['canonical_files']) != 1213 or OMIT.intersection(original['canonical_files']):
            raise ValueError('Unexpected canonical input or attempted canonical omission')
        shutil.copytree(base, output)
        for name in OMIT:
            (output / name).unlink()
        index = json.loads((output / 'native/skills.json').read_text())
        if len(index) != 62 or len({row['name'] for row in index}) != 62:
            raise ValueError('Expected Chief of Staff plus 61 specialists')
        for row in index:
            if row['canonical'] not in original['canonical_files']:
                raise ValueError('Workflow is not in the canonical source inventory')
            name = 'skills/' + row['name'] + '/scripts/run.py'
            data, executable = pinned_file(native_source, NATIVE, 'copilot/plugin/' + name)
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(0o755 if executable else 0o644)
            skill = output / 'skills' / row['name'] / 'SKILL.md'
            text = skill.read_text()
            if not text.startswith('---\n'):
                raise ValueError('Native skill lacks its original frontmatter')
            end = text.index('\n---\n', 4) + len('\n---\n')
            body = ('\nLoad the [canonical workflow](../../' + row['canonical'] + ') and its companion resources. '
                    'Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.\n\n')
            if row['name'] == 'chief-of-staff':
                body += ('Use the [guarded routing entrypoint](scripts/run.py), for example '
                         '`python <resolved-entrypoint> intake "review this code" --json`. '
                         'It selects the canonical working directory and returns an assignment without performing specialist work.\n\n')
            else:
                body += ('For a local Python helper, use the [guarded role entrypoint](scripts/run.py): '
                         '`python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. '
                         'Use `--context` to locate the canonical role folder for other documented tools.\n\n')
            body += ('The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. '
                     'Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, '
                     'remote access, credential changes or scheduled work.\n')
            skill.write_text(text[:end] + body)
        entry, executable = pinned_file(native_source, NATIVE, 'tools/harness-assets/openclaw.mjs')
        (output / 'native/openclaw.mjs').write_bytes(entry)
        (output / 'native/openclaw.mjs').chmod(0o755 if executable else 0o644)
        icon, _ = pinned_file(native_source, NATIVE, 'tools/harness-assets/openclaw-icon.png')
        from PIL import Image
        import io
        with Image.open(output / 'assets/native-plugin-icon.png') as original_icon, Image.open(io.BytesIO(icon)) as optimized:
            if original_icon.size != optimized.size or original_icon.convert('RGBA').tobytes() != optimized.convert('RGBA').tobytes():
                raise ValueError('OpenClaw listing icon differs from the original pixels')
            for field in ['icc_profile', 'gamma', 'srgb', 'chromaticity']:
                if original_icon.info.get(field) != optimized.info.get(field):
                    raise ValueError('Listing icon colour metadata differs: ' + field)
        if len(icon) > 512 * 1024:
            raise ValueError('Listing icon exceeds the provider byte limit')
        (output / 'assets/icon.png').write_bytes(icon)
        # Reuse the reviewed strict source-CI relocation. Canonical notices remain
        # at their original paths because this format creates no license aliases.
        metadata_source, _ = pinned_file(native_source, NATIVE, 'tools/distribution_metadata.py')
        metadata_path = temporary / 'distribution_metadata.py'
        metadata_path.write_bytes(metadata_source)
        spec = importlib.util.spec_from_file_location('reviewed_distribution_metadata', metadata_path)
        metadata = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(metadata)
        relocated = metadata.relocate_source_ci(output)
    package = {
        'name': 'solaris-dev-shop-openclaw', 'version': VERSION, 'type': 'module', 'license': 'MIT',
        'main': './native/openclaw.mjs',
        'description': '61 specialist workflows and a Chief of Staff with local recovery and evidence tools.',
        'author': {'name': 'Solaris Technologies', 'email': 'shehryar@solaristek.com', 'url': 'https://solaristek.com'},
        'repository': {'type': 'git', 'url': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins.git', 'directory': 'harnesses/openclaw'},
        'homepage': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins',
        'keywords': ['solaris-dev-shop', 'agent-skills', 'openclaw-plugin'],
        'openclaw': {'extensions': ['./native/openclaw.mjs'], 'compat': {'pluginApi': '>=2026.10.5 <2027'},
                     'build': {'openclawVersion': '2026.10.5'}},
    }
    write_json(output / 'package.json', package)
    write_json(output / 'openclaw.plugin.json', {
        'id': 'solaris-dev-shop', 'name': 'Solaris Dev Shop', 'version': VERSION,
        'description': package['description'], 'skills': ['./skills'], 'categories': ['developer-tools'],
        'configSchema': {'type': 'object', 'additionalProperties': False, 'properties': {}},
        'cliCommands': [{'name': 'solaris', 'description': 'Route a request through the pinned Solaris coordinator', 'hasSubcommands': True}]})
    (output / 'README.md').write_text(
        '# Solaris Dev Shop for OpenClaw\n\n'
        'Chief of Staff plus 61 specialists: one complete plugin with 62 workflows. '
        'All canonical helpers, references, licenses, fixtures and tests remain in this package. '
        'Skills reference shared canonical resources within the plugin; no Copilot-only resource mirrors are needed.\n\n'
        '## Optional specialist setup\n\n'
        'Specialist operations run only when requested for a specific task using the host tools and permissions. '
        'Unity licence activation is an optional manual setup workflow: the operator controls the Unity account, '
        'licence-file upload and repository secret. Local encrypted-DNS setup is a separate optional network-administration task '
        'requiring authorization for the selected resolver and network. Neither feature starts or receives credentials on plugin installation. '
        'Review the intended destination, credential scope and configuration before activating either workflow.\n\n'
        'The native `solaris intake` command returns a bounded assignment and does not execute specialist work. '
        'Loading the plugin installs no service, container, scheduler, updater or MCP connection and grants no account access. '
        'Host tools and permission checks apply. Local Python helpers require Python 3.10+ and their documented prerequisites.\n\n'
        'Core source: ' + CORE + '. Reviewed native adapter and guarded entrypoints: ' + NATIVE + '. '
        'SOLARIS-BUILD-SOURCE.json binds all 1213 canonical hashes; HARNESS-BUILD.json binds generated files and modes. '
        'A prepared candidate is not ClawHub approval or a completed security scan.\n\n'
        'MIT licensed. Solaris Technologies, https://solaristek.com. '
        'Support: https://github.com/Shaisolaris/solaris-dev-shop-plugins/issues.\n')
    provenance = json.loads((output / 'SOLARIS-BUILD-SOURCE.json').read_text())
    for name, expected in provenance['canonical_files'].items():
        if sha((output / name).read_bytes()) != expected:
            raise ValueError('Canonical source differs: ' + name)
    if list((output / 'skills').glob('*/resources/canonical')):
        raise ValueError('Unexpected redundant resource mirror')
    record = {'host': 'openclaw', 'version': VERSION, 'core_source': CORE, 'native_source': NATIVE,
              'reviewed_packager': PACKAGER, 'layout': 'shared-canonical', 'canonical_files': 1213,
              'specialists': 61, 'coordinator': 1, 'new_employee_capabilities': 0,
              'canonical_notice': 'NOTICE.md', 'redundant_resource_aliases': [],
              'relocated_repository_configuration': relocated, 'omitted_other_provider_files': sorted(OMIT),
              'files': inventory(output)}
    write_json(output / 'HARNESS-BUILD.json', record)
    return {'host': 'openclaw', 'files': len(record['files']) + 1, 'canonical_files': 1213,
            'workflows': 62, 'source': CORE, 'version': VERSION}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--packager', type=Path, required=True)
    parser.add_argument('--native-source', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.packager, args.native_source, args.output)))
