#!/usr/bin/env python3
"""Private negative controls for official exact classification; scanned code is never executed."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import time
from types import SimpleNamespace

import nvidia_h74_exact_classification as C


def controls(args):
    summary = C.read(args.classified / 'CLASSIFIED-SUMMARY.json')
    if (summary.get('completeSafeScopes'), summary.get('exactPhysicalFilesCovered'),
            summary.get('reviewedFindingsClassified')) != (9, 1348, 846):
        raise ValueError('All exact complete classified scans must precede controls')
    scanner = C.DRIVER.verify_runtime(args.runtime)
    if C.sha(args.parser_bin / 'shfmt') != C.DRIVER.SHFMT_SHA256:
        raise ValueError('Unreviewed Bash parser')
    manifest = C.read(args.scopes / 'partition.json')
    scope = next(x for x in manifest['scopes'] if x['id'] == 'scope-008')
    source = args.scopes / 'scopes/scope-008/input'
    original_baseline = args.classified / 'scope-008/official-baseline.json'
    baseline_hash = C.sha(original_baseline)
    raw = C.read(args.scopes / 'scopes/scope-008/raw-report.json')
    C.assert_complete(raw, source, scope['files'])
    args.output.mkdir(mode=0o700)
    cases = args.output / 'private-controls'
    cases.mkdir(mode=0o700)
    passed = []
    records = []
    def reject(label, operation):
        try:
            operation()
        except ValueError:
            passed.append(label)
        else:
            raise ValueError('Guard accepted the private negative control: ' + label)
    def case(label):
        folder = cases / label
        folder.mkdir(mode=0o700)
        root = folder / 'input'
        shutil.copytree(source, root)
        return folder, root
    def scan(label, folder, root, baseline=original_baseline):
        home = folder / 'home'
        home.mkdir(mode=0o700)
        env = {'PATH': str(scanner.parent) + ':' + str(args.parser_bin) + ':/usr/bin:/bin',
               'HOME': str(home), 'XDG_CACHE_HOME': str(home / 'cache'), 'LANG': 'en_US.UTF-8',
               'PYTHONUNBUFFERED': '1', 'SKILLSPECTOR_BUILD_REVISION': C.DRIVER.SCANNER_RELEASE}
        report_path = folder / 'vendor-report.json'
        command = [str(scanner), 'scan', str(root), '--output', str(report_path), '--baseline', str(baseline),
                   '--show-suppressed', *C.DRIVER.STRICT_FLAGS]
        start = time.monotonic()
        with (folder / 'stdout.log').open('x') as out, (folder / 'stderr.log').open('x') as err:
            code = subprocess.run(command, cwd=folder, env=env, stdout=out, stderr=err, timeout=720).returncode
        record = {'label': label, 'command': command, 'exit': code,
                  'seconds': round(time.monotonic() - start, 3), 'reportSha256': C.sha(report_path)}
        records.append(record)
        (args.output / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
        if C.sha(original_baseline) != baseline_hash:
            raise ValueError('Original baseline changed')
        return code, C.read(report_path)
    folder, root = case('source-byte-drift')
    canary = root / 'tests/test_child_environment_scope.py'
    canary.write_bytes(canary.read_bytes() + b'\n# Private source-change control, never a release input.\n')
    code, report = scan('source-byte-drift', folder, root)
    C.assert_complete(report, root, C.DRIVER.inventory(root))
    active = {x['id'] for x in report['issues'] if x['location']['file'] == 'tests/test_child_environment_scope.py'}
    if code != 1 or not {'AST8', 'AST2', 'AST6', 'AST4'} <= active:
        raise ValueError('Changed source did not reactivate every canary rule')
    passed.append('official-source-byte-drift-reactivates-four-rules')
    folder, root = case('new-unexecuted-finding')
    new = root / 'tests/zz_private_known_finding.py'
    new.write_text('def never_invoked_private_control():\n    return eval("1 + 1")\n')
    code, report = scan('new-unexecuted-finding', folder, root)
    C.assert_complete(report, root, C.DRIVER.inventory(root))
    if code != 1 or not any(x['id'] == 'AST2' and x['location']['file'] == 'tests/zz_private_known_finding.py'
                            for x in report['issues']):
        raise ValueError('New unreviewed finding disappeared')
    passed.append('official-new-unexecuted-finding-remains-active')
    folder, root = case('required-opaque-primary')
    primary = root / 'private-required/SKILL.md'
    primary.parent.mkdir()
    primary.write_bytes(b'\xff\xfe' + 'Private benign unsupported primary input'.encode('utf-16-le'))
    code, report = scan('required-opaque-primary', folder, root)
    if code != 2 or report.get('analysis_completeness', {}).get('is_complete') is not False:
        raise ValueError('Required opaque input was not natively rejected')
    reject('native-incomplete-cannot-be-classified-clear',
           lambda: C.assert_complete(report, root, C.DRIVER.inventory(root)))
    folder, root = case('baseline-version-tamper')
    baseline = folder / 'private-tampered-baseline.json'
    data = C.read(original_baseline)
    data['scanner_version'] = 'PRIVATE-WRONG-SCANNER-VERSION'
    baseline.write_text(json.dumps(data))
    code, report = scan('baseline-version-tamper', folder, root, baseline)
    C.assert_complete(report, root, scope['files'])
    if code != 1 or report.get('suppressed_count') != 0 or len(report['issues']) != len(raw['issues']):
        raise ValueError('Tampered scanner version suppressed findings')
    passed.append('official-wrong-baseline-scanner-version-reactivates-all-findings')
    folder, root = case('inventory-guards')
    target = root / 'tests/test_child_environment_scope.py'
    original = target.read_bytes()
    def check_inventory():
        if C.DRIVER.inventory(root) != scope['files']:
            raise ValueError('Exact inventory differs')
    target.unlink()
    reject('missing-physical-source-refused', check_inventory)
    target.write_bytes(original + b'\n# byte drift\n')
    reject('changed-source-hash-refused', check_inventory)
    target.write_bytes(original)
    target.chmod(0o755)
    reject('changed-executable-mode-refused', check_inventory)
    target.chmod(0o644)
    extra = root / 'private-extra.txt'
    extra.write_text('private extra data')
    reject('extra-physical-source-refused', check_inventory)
    extra.unlink()
    target.unlink()
    target.symlink_to(source / 'tests/test_child_environment_scope.py')
    reject('symbolic-link-input-refused', check_inventory)
    mutations = {
        'native-false-completeness-refused': lambda x: x['analysis_completeness'].update(is_complete=False),
        'wrong-scanner-report-refused': lambda x: x['metadata'].update(skillspector_version='PRIVATE-WRONG-VERSION'),
        'boolean-analyzer-counter-refused': lambda x: x['analysis_completeness']['analyzer_statuses'][0].update(completed=True),
        'analyzer-work-gap-refused': lambda x: x['analysis_completeness']['analyzer_statuses'][0].update(unaccounted=1),
    }
    for label, mutate in mutations.items():
        changed = copy.deepcopy(raw)
        mutate(changed)
        reject(label, lambda: C.assert_complete(changed, source, scope['files']))
    fake_runtime = cases / 'private-untrusted-runtime'
    fake_runtime.mkdir()
    (fake_runtime / 'skillspector-2.13.2.tar.gz').write_bytes(b'private invalid identity control')
    reject('untrusted-scanner-artifact-refused', lambda: C.DRIVER.verify_runtime(fake_runtime))
    review = C.read(args.review)
    first = next(iter(review['findings']))
    for label, change in (
        ('unresolved-finding-refused', lambda x: x['findings'][first].update(disposition='needs-verification')),
        ('missing-finding-disposition-refused', lambda x: x['findings'].pop(first)),
        ('changed-review-source-hash-refused', lambda x: x['findings'][first].update(source_sha256='0' * 64)),
    ):
        changed = copy.deepcopy(review)
        change(changed)
        review_path = cases / (label + '.json')
        review_path.write_text(json.dumps(changed))
        output = cases / (label + '-must-not-exist')
        parameters = SimpleNamespace(scopes=args.scopes, review=review_path, candidate=args.candidate,
            runtime=args.runtime, parser_bin=args.parser_bin, output=output)
        reject(label, lambda: C.classify(parameters))
        if output.exists():
            raise ValueError('An unresolved review reached baseline output creation')
    C.DRIVER.verify_runtime(args.runtime)
    C.DRIVER.validate_git(args.candidate, C.ROOT, C.REVISION)
    if C.DRIVER.inventory(source) != scope['files'] or C.sha(original_baseline) != baseline_hash:
        raise ValueError('Original evidence changed during controls')
    receipt = {'controlsPassed': passed, 'actualVendorCommands': records,
               'sourcePackageUnchanged': True, 'originalBaselineUnchanged': True,
               'scannerSourceUnchanged': True, 'privateControlCodeExecuted': False,
               'providerApproval': False, 'releaseClearance': False,
               'note': 'Control evidence only; release decision must also reconcile all nine classified scopes and whole-report limitations.'}
    (args.output / 'CONTROL-RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return {k: v for k, v in receipt.items() if k != 'actualVendorCommands'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('scopes', 'review', 'candidate', 'runtime', 'parser-bin', 'classified', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    for name in vars(args):
        setattr(args, name, getattr(args, name).resolve())
    print(json.dumps(controls(args), indent=2))
