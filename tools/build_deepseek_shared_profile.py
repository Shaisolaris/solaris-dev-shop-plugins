#!/usr/bin/env python3
"""Prepare the existing DSH profile from the reviewed complete shared source.

Writes a new candidate directory only; never installs or publishes anything.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

SOURCE = '113540a3064ecb8037b58ff700955491367f704b'
CORE = 'dea39818dd09b2059266e44f39def0ecf6ca8151'
NATIVE = 'e02d8002d195f929e30fb5063bd04d4ed27190d6'
VERSION = '0.70.0'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pinned_file(repo, revision, name):
    row = git(repo, 'ls-tree', revision, '--', name).decode().strip()
    if not row or row.split()[0] not in {'100644', '100755'}:
        raise ValueError('Missing or non-regular pinned input: ' + name)
    return git(repo, 'show', revision + ':' + name), row.split()[0] == '100755'


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in candidate')
        if path.is_file():
            result[path.relative_to(root).as_posix()] = {
                'sha256': digest(path.read_bytes()),
                'executable': bool(path.stat().st_mode & 0o111)}
    return result


def build(repo, output):
    output = output.resolve()
    if output.exists():
        raise ValueError('Output must be a new directory')
    archive = git(repo, 'archive', SOURCE + ':harnesses/openclaw')
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        for entry in stream:
            if entry.isdir():
                continue
            path = Path(entry.name)
            if not entry.isfile() or path.is_absolute() or '..' in path.parts or entry.name in files:
                raise ValueError('Unsafe or duplicate source entry')
            files[entry.name] = (stream.extractfile(entry).read(), entry.mode & 0o777)
    if len(files) != 1337:
        raise ValueError('Unexpected complete source inventory')
    provenance = json.loads(files['SOLARIS-BUILD-SOURCE.json'][0])
    if provenance['source_commit'] != CORE or len(provenance['canonical_files']) != 1203:
        raise ValueError('Unexpected canonical source binding')
    original_record = json.loads(files['HARNESS-BUILD.json'][0])
    if original_record['core_source'] != CORE or original_record['native_source'] != NATIVE:
        raise ValueError('Unexpected reviewed native source')
    omitted = {'openclaw.plugin.json', 'native/openclaw.mjs', 'HARNESS-BUILD.json'}
    if omitted.intersection(provenance['canonical_files']):
        raise ValueError('Cannot omit canonical source')
    for name, (data, mode) in files.items():
        if name not in omitted:
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(mode)
    package_bytes, _ = pinned_file(repo, NATIVE, 'harnesses/deepseek/package.json')
    package = json.loads(package_bytes)
    if package['name'] != 'dsh-plugin-solaris-dev-shop' or package['dsh']['bundle']['patch'] != './cordis.patch.yml':
        raise ValueError('Unexpected existing DSH identity')
    package['version'] = VERSION
    (output / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
    for source, destination in [('tools/harness-assets/deepseek.mjs', 'native/deepseek.mjs'),
                                ('harnesses/deepseek/cordis.patch.yml', 'cordis.patch.yml')]:
        data, executable = pinned_file(repo, NATIVE, source)
        target = output / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o755 if executable else 0o644)
    (output / 'README.md').write_text(
        '# Solaris Dev Shop for DeepSeek Harness\n\n'
        'One complete plugin: 61 specialists and Chief of Staff. Version ' + VERSION + '.\n\n'
        'The existing Cordis provider registers all 62 canonical workflows and their contained resource folders. '
        'All canonical helpers, references, fixtures, tests and licences are preserved once in the shared layout. '
        'Host tools and permissions apply; installation starts no service, scheduled job or account connection.\n\n'
        'Core source: ' + CORE + '. Reviewed adapter: ' + NATIVE + '. '
        'SOLARIS-BUILD-SOURCE.json binds all 1203 canonical file hashes; HARNESS-BUILD.json binds generated files and modes. '
        'This candidate and its local validation are separate from public catalog acceptance and installation.\n')
    for name, expected in provenance['canonical_files'].items():
        if digest((output / name).read_bytes()) != expected:
            raise ValueError('Canonical source changed: ' + name)
    index = json.loads((output / 'native/skills.json').read_text())
    if len(index) != 62 or len({row['name'] for row in index}) != 62:
        raise ValueError('Expected 61 specialists and Chief of Staff')
    record = {'host': 'deepseek', 'version': VERSION, 'core_source': CORE,
              'native_source': NATIVE, 'reviewed_shared_source': SOURCE,
              'reviewed_packager': original_record['reviewed_packager'],
              'layout': 'shared-canonical', 'canonical_files': 1203,
              'specialists': 61, 'coordinator': 1, 'new_employee_capabilities': 0,
              'omitted_other_provider_files': sorted(omitted), 'files': inventory(output)}
    (output / 'HARNESS-BUILD.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    return {'host': 'deepseek', 'version': VERSION, 'files': len(record['files']) + 1,
            'canonical_files': 1203, 'workflows': 62, 'provider_admission': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output)))
