#!/usr/bin/env python3
"""Stage lossless scan scopes and run the unchanged NVIDIA CLI.

This raw-evidence driver never accepts findings or issues a release clearance.
NVIDIA 2.13.2 has no --min-coverage flag: the supported fail-on-incomplete flag
and the independent exact 100-percent report check both remain mandatory.
Reports and the partition manifest remain outside every scanned input.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import time
import tarfile

SCANNER_RELEASE = 'v2.13.2'
SCANNER_VERSION = '2.13.2'
SCANNER_SDIST_SHA256 = 'a08ffad0998e6e94578a7dc747be30a80f7db251e833c5900af585dbc7ef400e'
SHFMT_SHA256 = 'b7c872db63553ccffc7253aba3ed7d4885a27d83f1ba567b1138c6315a5847e5'
STRICT_FLAGS = ['--no-llm', '--format', 'json', '--fail-on-incomplete',
                '--fail-on-findings']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    result = {}
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Use a regular input directory')
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symbolic link in scan input')
        if path.is_file():
            raw = path.read_bytes()
            result[path.relative_to(root).as_posix()] = {
                'sha256': digest(raw), 'bytes': len(raw),
                'executable': bool(path.stat().st_mode & 0o111)}
    return result


def validate_git(candidate, repository, revision):
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Use the immutable full commit SHA')
    if subprocess.check_output(['git', '-C', str(repository), 'cat-file', '-t', revision]).strip() != b'commit':
        raise ValueError('The expected revision must be a commit')
    tree = subprocess.check_output(
        ['git', '-C', str(repository), 'ls-tree', '-rz', revision + ':harnesses/openclaw'])
    expected = {}
    for row in tree.split(b'\0'):
        if not row:
            continue
        header, encoded = row.split(b'\t', 1)
        mode, kind, object_id = header.decode().split()
        name = encoded.decode()
        path = PurePosixPath(name)
        if kind != 'blob' or mode not in ('100644', '100755') or path.is_absolute() or '..' in path.parts:
            raise ValueError('Non-regular or unsafe Git input')
        if name in expected:
            raise ValueError('Duplicate Git path')
        expected[name] = (object_id, mode == '100755')
    actual = inventory(candidate)
    if set(actual) != set(expected):
        raise ValueError('Candidate paths differ from immutable Git tree')
    for name, (object_id, executable) in expected.items():
        raw = (candidate / name).read_bytes()
        if hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() != object_id:
            raise ValueError('Candidate bytes differ from Git: ' + name)
        if actual[name]['executable'] != executable:
            raise ValueError('Candidate executable mode differs from Git: ' + name)
    record = json.loads((candidate / 'HARNESS-BUILD.json').read_text())
    if (record['specialists'], record['coordinator']) != (61, 1):
        raise ValueError('The fixed 61+1 scope changed')
    return actual


def verify_runtime(runtime):
    archive = runtime / 'skillspector-2.13.2.tar.gz'
    if digest(archive.read_bytes()) != SCANNER_SDIST_SHA256:
        raise ValueError('Unexpected official NVIDIA source distribution')
    source_root = runtime / 'skillspector-2.13.2'
    expected_package = set()
    with tarfile.open(archive) as stream:
        for entry in stream.getmembers():
            if not entry.isfile():
                continue
            parts = PurePosixPath(entry.name).parts[1:]
            relative = PurePosixPath(*parts)
            if not parts or relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe vendor archive path')
            source = source_root / relative
            if source.is_symlink() or source.read_bytes() != stream.extractfile(entry).read():
                raise ValueError('NVIDIA source was modified: ' + str(relative))
            if relative.parts[:2] == ('src', 'skillspector'):
                expected_package.add(str(relative))
    actual_package = {path.relative_to(source_root).as_posix()
                      for path in (source_root / 'src/skillspector').rglob('*')
                      if path.is_file() and '__pycache__' not in path.parts}
    if actual_package != expected_package:
        raise ValueError('Unexpected files in the NVIDIA implementation')
    scanner = source_root / '.venv/bin/skillspector'
    if not scanner.is_file():
        raise ValueError('The locked NVIDIA installation is missing')
    return scanner

def prepare(candidate, repository, revision, output, maximum):
    if output.exists():
        raise ValueError('Use a new evidence directory; preserve earlier runs')
    files = validate_git(candidate, repository, revision)
    output.mkdir(parents=True)
    entries = list(files)
    scopes = []
    for start in range(0, len(entries), maximum):
        scope_id = 'scope-%03d' % len(scopes)
        root = output / 'scopes' / scope_id / 'input'
        chosen = entries[start:start + maximum]
        for name in chosen:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(candidate / name, target)
            target.chmod(0o755 if files[name]['executable'] else 0o644)
        expected = {name: files[name] for name in chosen}
        if inventory(root) != expected:
            raise ValueError('Staged bytes or modes changed')
        scopes.append({'id': scope_id, 'files': expected})
    merged = {}
    for scope in scopes:
        if set(merged).intersection(scope['files']):
            raise ValueError('Overlapping partition paths')
        merged.update(scope['files'])
    if merged != files or inventory(candidate) != files:
        raise ValueError('The partition is not the exact immutable package')
    manifest = {'schema': 'solaris.nvidia-complete-scopes/1', 'revision': revision,
                'source_path': 'harnesses/openclaw', 'scanner_release': SCANNER_RELEASE,
                'scanner_sdist_sha256': SCANNER_SDIST_SHA256, 'flags': STRICT_FLAGS,
                'physical_files': len(files), 'files': files, 'scopes': scopes,
                'baseline_used': False, 'clearance': False}
    (output / 'partition.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return {'staged_files': len(files), 'scopes': len(scopes), 'clearance': False}


def run_raw(output, runtime, parser_bin, workers):
    scanner = verify_runtime(runtime)
    if digest((parser_bin / 'shfmt').read_bytes()) != SHFMT_SHA256:
        raise ValueError('Unexpected Bash parser; this plan pins official Darwin arm64 shfmt 3.14.1')
    manifest = json.loads((output / 'partition.json').read_text())
    if (manifest['scanner_release'], manifest['scanner_sdist_sha256'], manifest['flags']) != (
            SCANNER_RELEASE, SCANNER_SDIST_SHA256, STRICT_FLAGS):
        raise ValueError('Mixed scanner configuration')

    def run_one(scope):
        folder = output / 'scopes' / scope['id']
        root = folder / 'input'
        if inventory(root) != scope['files']:
            raise ValueError('Scope source drift: ' + scope['id'])
        report = folder / 'raw-report.json'
        receipt_path = folder / 'raw-receipt.json'
        if report.exists() or receipt_path.exists():
            raise ValueError('Refusing to overwrite previous evidence')
        home = folder / 'home'
        home.mkdir(mode=0o700)
        environment = {'PATH': str(scanner.parent) + ':' + str(parser_bin) + ':/usr/bin:/bin',
                       'HOME': str(home), 'XDG_CACHE_HOME': str(home / 'cache'),
                       'LANG': 'en_US.UTF-8', 'PYTHONUNBUFFERED': '1',
                       'SKILLSPECTOR_BUILD_REVISION': SCANNER_RELEASE}
        command = [str(scanner), 'scan', str(root), '--output', str(report)] + STRICT_FLAGS
        started = time.monotonic()
        with (folder / 'raw.stdout.log').open('x') as stdout, (folder / 'raw.stderr.log').open('x') as stderr:
            try:
                code = subprocess.run(command, cwd=folder, env=environment,
                                      stdout=stdout, stderr=stderr, timeout=720).returncode
            except subprocess.TimeoutExpired:
                code = None
        source_unchanged = inventory(root) == scope['files']
        parsed = json.loads(report.read_text()) if report.is_file() else {}
        completeness = parsed.get('analysis_completeness', {})
        paths = {entry['path'] for entry in parsed.get('components', [])}
        missing = sorted(set(scope['files']) - paths)
        exceptions = completeness.get('ledger_exceptions', [])
        contract_errors = []
        optional_llm = {'meta_analyzer', 'semantic_developer_intent',
                        'semantic_security_discovery', 'semantic_quality_policy'}
        for status in completeness.get('analyzer_statuses', []):
            counters = [status.get(key) for key in ('planned_work', 'completed', 'partial',
                                                   'skipped', 'failed', 'unaccounted')]
            if not all(isinstance(value, int) and value >= 0 for value in counters):
                contract_errors.append(status.get('analyzer_id'))
                continue
            planned, completed, partial, skipped, failed, unaccounted = counters
            if planned != completed + partial + skipped + failed + unaccounted:
                contract_errors.append(status.get('analyzer_id'))
            if status.get('status') == 'completed' and (partial or failed or unaccounted):
                contract_errors.append(status.get('analyzer_id'))
            if status.get('status') == 'disabled' and status.get('analyzer_id') not in optional_llm:
                contract_errors.append(status.get('analyzer_id'))
        metadata = parsed.get('metadata', {})
        complete = (source_unchanged and not missing and parsed.get('execution_successful') is True
                    and not contract_errors and metadata.get('llm_requested') is False
                    and metadata.get('skillspector_version') == SCANNER_VERSION
                    and not completeness.get('scope_exclusions')
                    and completeness.get('is_complete') is True
                    and completeness.get('coverage_percent') == 100
                    and completeness.get('partially_inspected_files') == 0
                    and completeness.get('entirely_uninspected_files') == 0
                    and not any(x.get('outcome') in ('partial', 'failed') for x in exceptions))
        receipt = {'id': scope['id'], 'command': command, 'exit_code': code,
                   'wall_seconds': round(time.monotonic() - started, 3),
                   'scanner_release': SCANNER_RELEASE, 'scanner_sdist_sha256': SCANNER_SDIST_SHA256,
                   'source_unchanged': source_unchanged, 'missing_physical_components': missing,
                   'analyzer_contract_errors': contract_errors,
                   'complete_in_scope': complete, 'analysis_completeness': completeness,
                   'findings': len(parsed.get('issues', [])),
                   'report_sha256': digest(report.read_bytes()) if report.exists() else None,
                   'reported_model_calls': metadata.get('llm_calls_attempted'),
                   'credentials_forwarded': False, 'baseline_used': False, 'clearance': False}
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
        return receipt

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(run_one, manifest['scopes']))
    verify_runtime(runtime)
    if digest((parser_bin / 'shfmt').read_bytes()) != SHFMT_SHA256:
        raise ValueError('The Bash parser changed during the run')
    summary = {'scopes': len(results), 'complete_scopes': sum(x['complete_in_scope'] for x in results),
               'incomplete_scope_ids': [x['id'] for x in results if not x['complete_in_scope']],
               'physical_files': manifest['physical_files'], 'baseline_used': False,
               'findings_not_yet_classified': sum(x['findings'] for x in results), 'clearance': False}
    (output / 'raw-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='mode', required=True)
    stage = commands.add_parser('prepare')
    for name in ('candidate', 'repository', 'output'):
        stage.add_argument('--' + name, type=Path, required=True)
    stage.add_argument('--revision', required=True)
    stage.add_argument('--max-files', type=int, default=150, choices=range(1, 301))
    raw = commands.add_parser('run-raw')
    for name in ('output', 'runtime', 'parser-bin'):
        raw.add_argument('--' + name, type=Path, required=True)
    raw.add_argument('--workers', type=int, default=2, choices=(1, 2, 3, 4))
    args = parser.parse_args()
    result = prepare(args.candidate.resolve(), args.repository.resolve(), args.revision,
                     args.output.resolve(), args.max_files) if args.mode == 'prepare' else run_raw(
                         args.output.resolve(), args.runtime.resolve(), args.parser_bin.resolve(), args.workers)
    print(json.dumps(result, indent=2))
