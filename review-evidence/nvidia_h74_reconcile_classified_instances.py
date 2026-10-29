#!/usr/bin/env python3
"""Read-only reconciliation of native pre-dedup suppressed instances.

NVIDIA report.py deduplicates active findings after baseline partitioning, while
retaining pre-dedup suppressed instances. Preserve every original vendor record;
only byte-identical public finding identities may repeat. No scanner is invoked.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess

import nvidia_h74_exact_classification as C


def assert_instances(report, raw):
    instances = report.get('suppressed', [])
    if (report.get('issues') or type(report.get('suppressed_count')) is not int
            or report['suppressed_count'] != len(instances)):
        raise ValueError('Active findings or inconsistent native suppression count')
    expected = Counter(map(C.issue_identity, raw['issues']))
    actual = Counter(map(C.issue_identity, instances))
    if set(actual) != set(expected) or any(actual[key] < count for key, count in expected.items()):
        raise ValueError('A finding identity is missing or an unreviewed identity was suppressed')
    risk = report.get('risk_assessment', {})
    if risk.get('score') != 0 or risk.get('recommendation') != 'SAFE':
        raise ValueError('Native risk is not zero/SAFE')
    duplicates = [{'finding': json.loads(key), 'rawInstances': expected[key],
                   'nativeSuppressedInstances': count}
                  for key, count in actual.items() if count != expected[key]]
    return {'reviewedUniqueFindings': len(expected), 'nativeSuppressedInstances': len(instances),
            'identicalDuplicateInstances': sum(actual.values()) - sum(expected.values()),
            'duplicateEvidence': duplicates, 'noMissingOrNewFindingIdentities': True}


def reconcile(args):
    C.DRIVER.verify_runtime(args.runtime)
    if C.sha(args.parser_bin / 'shfmt') != C.DRIVER.SHFMT_SHA256:
        raise ValueError('Unreviewed parser')
    frozen = C.DRIVER.validate_git(args.candidate, C.ROOT, C.REVISION)
    manifest = C.read(args.scopes / 'partition.json')
    if (manifest.get('revision') != C.REVISION or manifest.get('physical_files') != 1348
            or manifest.get('files') != frozen or len(manifest.get('scopes', [])) != 9
            or manifest.get('flags') != C.DRIVER.STRICT_FLAGS
            or manifest.get('scanner_sdist_sha256') != C.DRIVER.SCANNER_SDIST_SHA256):
        raise ValueError('Mixed input/source/scanner')
    review = C.read(args.review)
    if review.get('source_revision') != C.REVISION or review.get('scanner_version') != C.VERSION:
        raise ValueError('Wrong review binding')
    digest = C.sha(args.review)
    reason = ('Exact contextual false positives individually reviewed in sidecar SHA256 ' + digest
              + '; source ' + C.REVISION + '; original findings ' + C.RAW_EVIDENCE
              + '. Reasons and source hashes are recorded per review key. No new findings or coverage gaps accepted.')
    keys = set()
    union = {}
    results = []
    for scope in manifest['scopes']:
        raw_path = args.scopes / 'scopes' / scope['id'] / 'raw-report.json'
        exact = subprocess.check_output(['git', '-C', str(C.ROOT), 'show',
            C.RAW_EVIDENCE + ':review-evidence/h74-nvidia-2132/' + scope['id'] + '-raw-report.json'])
        if raw_path.read_bytes() != exact:
            raise ValueError('Original vendor raw report changed')
        raw = C.read(raw_path)
        root = raw_path.parent / 'input'
        C.assert_complete(raw, root, scope['files'])
        for name, metadata in scope['files'].items():
            if name in union:
                raise ValueError('Overlapping scopes')
            union[name] = metadata
        for issue in raw['issues']:
            key = C.review_key(issue)
            row = review['findings'].get(key, {})
            if (key in keys or row.get('disposition') != 'contextual-false-positive'
                    or row.get('finding_id') != issue['finding_id']
                    or row.get('source_sha256') != C.sha_component(args.candidate, issue['location']['file'])
                    or not isinstance(row.get('reason'), str) or len(row['reason'].strip()) < 32
                    or len(issue.get('occurrences', [])) != 1):
                raise ValueError('Missing, unresolved or drifted exact disposition')
            keys.add(key)
        folder = args.classified / scope['id']
        commands = C.read(folder / 'commands.json')
        if [x.get('label') for x in commands] != ['generate', 'classified'] or any(x.get('exit') != 0 for x in commands):
            raise ValueError('Original official generation/scan did not both terminate successfully')
        baseline = folder / 'official-baseline.json'
        C.assert_baseline(C.read(baseline), raw['issues'], reason)
        if 'Scan analysis is incomplete' in (folder / 'generate.stderr.log').read_text():
            raise ValueError('Baseline generation was incomplete')
        report_path = folder / 'classified-report.json'
        report = C.read(report_path)
        media = C.assert_complete(report, root, scope['files'])
        counts = assert_instances(report, raw)
        if not all(x.get('suppression_reason') == reason for x in report['suppressed']):
            raise ValueError('Suppression lost its per-key sidecar binding')
        receipt = {'scope': scope['id'], 'physicalFiles': len(scope['files']), 'nativeExit': 0,
                   'nativeComplete': True, 'nativeCoverage': 100, 'recommendation': 'SAFE', 'score': 0,
                   'activeFindings': 0, 'baselineSha256': C.sha(baseline), 'reportSha256': C.sha(report_path),
                   'reviewSidecarSha256': digest, 'media': media, **counts,
                   'nativeReportsAndBaselinesUnchanged': True, 'scannerInvokedByReconciler': False,
                   'releaseClearance': False}
        output = folder / 'RECONCILED-RECEIPT.json'
        with output.open('x') as stream:
            stream.write(json.dumps(receipt, indent=2) + '\n')
        results.append(receipt)
    if union != frozen or set(review['findings']) != keys or len(keys) != 846:
        raise ValueError('Source union or review identity set differs')
    C.DRIVER.verify_runtime(args.runtime)
    if C.DRIVER.validate_git(args.candidate, C.ROOT, C.REVISION) != frozen or C.sha(args.review) != digest:
        raise ValueError('Immutable source or independent review changed')
    summary = {'sourceRevision': C.REVISION, 'scannerVersion': C.VERSION, 'completeSafeScopes': 9,
               'exactPhysicalFilesCovered': len(union), 'reviewedFindingsClassified': len(keys),
               'nativeSuppressedInstances': sum(x['nativeSuppressedInstances'] for x in results),
               'identicalDuplicateInstances': sum(x['identicalDuplicateInstances'] for x in results),
               'allClassifiedScopesSafe': True, 'originalReportsRetained': True,
               'sourceUnchanged': True, 'vendorSourceUnchanged': True, 'controlsRequired': True,
               'releaseClearance': False, 'providerApproval': False, 'singleWholeReportComplete': False,
               'wholeReportLimitNotWaived': True,
               'consumerCorrection': 'Native active findings are deduplicated; suppressed instances are not. Exact identities, every source location and all vendor multiplicities remain preserved.'}
    with (args.classified / 'CLASSIFIED-SUMMARY.json').open('x') as stream:
        stream.write(json.dumps(summary, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('scopes', 'review', 'candidate', 'runtime', 'parser-bin', 'classified'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    for name in vars(args):
        setattr(args, name, getattr(args, name).resolve())
    print(json.dumps(reconcile(args), indent=2))
