#!/usr/bin/env python3
"""Run stock CLI exact baselines only after complete, exact-key source review.

Every vendor report/baseline stays unmodified and outside scanned inputs.
This stage cannot authorize publication: independent controls remain mandatory.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
REVISION = '1b3212f0ba9fc58f7675877be9cf0ea0d8283ee8'
RAW_EVIDENCE = 'c35a55549005cedd65827c88e1aec775a0c579dd'
VERSION = '2.13.2'
OPTIONAL_LLM = {'meta_analyzer', 'semantic_developer_intent', 'semantic_security_discovery', 'semantic_quality_policy'}


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


DRIVER = module('raw_scope_driver', ROOT / 'review-evidence/nvidia_2132_complete_scopes.py')
MEDIA = module('native_media_contract', ROOT / 'tools/validate_incidental_media.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key')
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def issue_identity(issue):
    ignored = {'finding_id', 'suppressed', 'suppression_reason'}
    return json.dumps({k: v for k, v in issue.items() if k not in ignored},
                      sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def review_key(issue):
    return hashlib.sha256(issue_identity(issue).encode()).hexdigest()


def assert_complete(report, root, files):
    if DRIVER.inventory(root) != files:
        raise ValueError('Exact scope bytes or executable modes changed')
    completeness = report.get('analysis_completeness', {})
    metadata = report.get('metadata', {})
    if (report.get('execution_successful') is not True or completeness.get('is_complete') is not True
            or completeness.get('coverage_percent') != 100
            or completeness.get('partially_inspected_files') != 0
            or completeness.get('entirely_uninspected_files') != 0
            or completeness.get('ledger_exceptions')
            or metadata.get('skillspector_version') != VERSION
            or metadata.get('llm_requested') is not False):
        raise ValueError('Native complete 100-percent inspection under exact static scanner is mandatory')
    if set(files) - {x['path'] for x in report.get('components', [])}:
        raise ValueError('A physical component is absent from the vendor report')
    statuses = completeness.get('analyzer_statuses', [])
    if not statuses:
        raise ValueError('Missing native analyzer accounting')
    for status in statuses:
        values = [status.get(k) for k in ('planned_work', 'completed', 'partial', 'skipped', 'failed', 'unaccounted')]
        if not all(type(x) is int and x >= 0 for x in values):
            raise ValueError('Invalid native analyzer counter')
        planned, completed, partial, skipped, failed, unaccounted = values
        if planned != completed + partial + skipped + failed + unaccounted:
            raise ValueError('Unaccounted analyzer work')
        if status.get('status') == 'disabled':
            if status.get('analyzer_id') not in OPTIONAL_LLM or planned:
                raise ValueError('Only optional LLM slots may be disabled in explicit no-LLM mode')
        elif partial or skipped or failed or unaccounted:
            raise ValueError('An applicable analyzer did not complete')
    return MEDIA.native_media_contract(report, root, files)


def assert_baseline(data, issues, reason):
    entries = data.get('fingerprints', [])
    if data.get('version') != 2 or data.get('scanner_version') != VERSION or data.get('rules') != []:
        raise ValueError('Only the official version-2 exact baseline is accepted; no glob rules')
    if len(entries) != len(issues) or len({x['hash'] for x in entries}) != len(entries):
        raise ValueError('Generated fingerprint count differs from the reviewed one-occurrence findings')
    if Counter((x['rule_id'], x['file']) for x in entries) != Counter((x['id'], x['location']['file']) for x in issues):
        raise ValueError('Generated baseline contains a different rule or component')
    if not all(re.fullmatch(r'sha256:[0-9a-f]{64}', x['hash']) and x.get('reason') == reason for x in entries):
        raise ValueError('Invalid generated fingerprint or unbound reason')


def assert_classified(report, raw):
    if report.get('issues') or report.get('suppressed_count') != len(raw['issues']):
        raise ValueError('Active, missing or unexpected finding after classification')
    suppressed = report.get('suppressed', [])
    if Counter(map(issue_identity, suppressed)) != Counter(map(issue_identity, raw['issues'])):
        raise ValueError('Suppressed vendor evidence differs from the reviewed original findings')
    risk = report.get('risk_assessment', {})
    if risk.get('score') != 0 or risk.get('recommendation') != 'SAFE':
        raise ValueError('Vendor did not return zero-risk SAFE')


def classify(args):
    scanner = DRIVER.verify_runtime(args.runtime)
    if sha(args.parser_bin / 'shfmt') != DRIVER.SHFMT_SHA256:
        raise ValueError('Unreviewed Bash parser')
    frozen = DRIVER.validate_git(args.candidate, ROOT, REVISION)
    manifest = read(args.scopes / 'partition.json')
    if (manifest.get('revision') != REVISION or manifest.get('physical_files') != 1348
            or manifest.get('files') != frozen or len(manifest.get('scopes', [])) != 9
            or manifest.get('flags') != DRIVER.STRICT_FLAGS
            or manifest.get('scanner_sdist_sha256') != DRIVER.SCANNER_SDIST_SHA256):
        raise ValueError('Mixed immutable source or scanner configuration')
    review = read(args.review)
    if review.get('source_revision') != REVISION or review.get('scanner_version') != VERSION:
        raise ValueError('Disposition record is not bound to this exact source and scanner')
    rows = review.get('findings', {})
    union = {}
    reports = {}
    expected_keys = set()
    for scope in manifest['scopes']:
        folder = args.scopes / 'scopes' / scope['id']
        path = folder / 'raw-report.json'
        exact = subprocess.check_output(['git', '-C', str(ROOT), 'show',
            RAW_EVIDENCE + ':review-evidence/h74-nvidia-2132/' + scope['id'] + '-raw-report.json'])
        if path.read_bytes() != exact:
            raise ValueError('Original raw report changed')
        report = read(path)
        assert_complete(report, folder / 'input', scope['files'])
        if report.get('suppressed_count') != 0:
            raise ValueError('Raw evidence already contains a baseline')
        reports[scope['id']] = report
        for name, value in scope['files'].items():
            if name in union:
                raise ValueError('Overlapping physical scopes')
            union[name] = value
        for issue in report['issues']:
            if len(issue.get('occurrences', [])) != 1:
                raise ValueError('This reviewed inventory requires one exact occurrence per row')
            key = review_key(issue)
            if key in expected_keys:
                raise ValueError('Duplicate finding review key')
            expected_keys.add(key)
            row = rows.get(key, {})
            if (row.get('disposition') != 'contextual-false-positive'
                    or not isinstance(row.get('reason'), str) or len(row['reason'].strip()) < 32
                    or row.get('source_sha256') != sha_component(args.candidate, issue['location']['file'])
                    or row.get('finding_id') != issue['finding_id']):
                raise ValueError('An exact finding is unreviewed, unresolved or actionable: ' + key)
    if union != frozen or len(expected_keys) != 846 or set(rows) != expected_keys:
        raise ValueError('Incomplete source union or extra/missing disposition keys')
    args.output.mkdir(mode=0o700)
    review_digest = sha(args.review)
    reason = ('Exact contextual false positives individually reviewed in sidecar SHA256 ' + review_digest
              + '; source ' + REVISION + '; original findings ' + RAW_EVIDENCE
              + '. Reasons and source hashes are recorded per review key. No new findings or coverage gaps accepted.')

    def run_scope(scope):
        folder = args.output / scope['id']
        folder.mkdir(mode=0o700)
        home = folder / 'home'
        home.mkdir(mode=0o700)
        root = args.scopes / 'scopes' / scope['id'] / 'input'
        env = {'PATH': str(scanner.parent) + ':' + str(args.parser_bin) + ':/usr/bin:/bin',
               'HOME': str(home), 'XDG_CACHE_HOME': str(home / 'cache'), 'LANG': 'en_US.UTF-8',
               'PYTHONUNBUFFERED': '1', 'SKILLSPECTOR_BUILD_REVISION': DRIVER.SCANNER_RELEASE}
        commands = []
        def run(label, arguments):
            command = [str(scanner), *arguments]
            started = time.monotonic()
            with (folder / (label + '.stdout.log')).open('x') as out, (folder / (label + '.stderr.log')).open('x') as err:
                code = subprocess.run(command, cwd=folder, env=env, stdout=out, stderr=err, timeout=720).returncode
            commands.append({'label': label, 'command': command, 'exit': code,
                             'seconds': round(time.monotonic() - started, 3)})
            (folder / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
            return code
        baseline = folder / 'official-baseline.json'
        code = run('generate', ['baseline', str(root), '--no-llm', '--output', str(baseline), '--reason', reason])
        if code != 0 or 'Scan analysis is incomplete' in (folder / 'generate.stderr.log').read_text():
            raise ValueError('Official baseline generation did not complete cleanly: ' + scope['id'])
        raw = reports[scope['id']]
        assert_baseline(read(baseline), raw['issues'], reason)
        baseline_digest = sha(baseline)
        report_path = folder / 'classified-report.json'
        code = run('classified', ['scan', str(root), '--output', str(report_path), '--baseline', str(baseline),
                                 '--show-suppressed', *DRIVER.STRICT_FLAGS])
        report = read(report_path)
        if code != 0 or sha(baseline) != baseline_digest:
            raise ValueError('Classified scan failed or baseline changed: ' + scope['id'])
        media = assert_complete(report, root, scope['files'])
        assert_classified(report, raw)
        if not all(x.get('suppression_reason') == reason for x in report['suppressed']):
            raise ValueError('A suppression reason lost its review-sidecar binding')
        receipt = {'scope': scope['id'], 'physicalFiles': len(scope['files']), 'exit': code,
                   'nativeComplete': True, 'nativeCoverage': 100, 'recommendation': 'SAFE', 'score': 0,
                   'activeFindings': 0, 'reviewedSuppressedFindings': len(report['suppressed']),
                   'baselineSha256': baseline_digest, 'reportSha256': sha(report_path),
                   'reviewSidecarSha256': review_digest, 'media': media,
                   'sourceUnchanged': True, 'noGlobRules': True, 'releaseClearance': False}
        (folder / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        return receipt
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run_scope, manifest['scopes']))
    if DRIVER.validate_git(args.candidate, ROOT, REVISION) != frozen or sha(args.review) != review_digest:
        raise ValueError('Immutable package or reviewed dispositions changed')
    DRIVER.verify_runtime(args.runtime)
    if sha(args.parser_bin / 'shfmt') != DRIVER.SHFMT_SHA256:
        raise ValueError('Bash parser changed')
    summary = {'sourceRevision': REVISION, 'scannerVersion': VERSION, 'completeSafeScopes': len(results),
               'exactPhysicalFilesCovered': sum(x['physicalFiles'] for x in results),
               'reviewedFindingsClassified': sum(x['reviewedSuppressedFindings'] for x in results),
               'allClassifiedScopesSafe': True, 'originalReportsRetained': True,
               'sourceUnchanged': True, 'vendorSourceUnchanged': True,
               'controlsRequired': True, 'releaseClearance': False, 'providerApproval': False,
               'singleWholeReportComplete': False, 'wholeReportLimitNotWaived': True}
    (args.output / 'CLASSIFIED-SUMMARY.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


def sha_component(root, name):
    import io
    import zipfile
    parts = name.split('!/')
    data = (root / parts[0]).read_bytes()
    for member in parts[1:]:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if sum(x.filename == member for x in archive.infolist()) != 1:
                raise ValueError('Ambiguous virtual member')
            data = archive.read(member)
    return hashlib.sha256(data).hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('scopes', 'review', 'candidate', 'runtime', 'parser-bin', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    for name in vars(args):
        setattr(args, name, getattr(args, name).resolve())
    print(json.dumps(classify(args), indent=2))
