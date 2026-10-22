#!/usr/bin/env python3
"""Check real composite-package license notices without changing the core checker."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CHECKER = 'employees/quality-security/security-auditor/provenance_check.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(package, host):
    baseline = json.loads((ROOT / 'plugin/SOLARIS-BUILD-SOURCE.json').read_text())
    original_notice = (ROOT / 'plugin/NOTICE.md').read_bytes()
    if digest(package / CHECKER) != baseline['canonical_files'][CHECKER]:
        raise ValueError('Unreviewed or no-op provenance checker')
    if (package / 'SOURCE-NOTICE.md').read_bytes() != original_notice:
        raise ValueError('Original canonical notice was not retained')
    if not (package / 'NOTICE.md').read_bytes().startswith(original_notice):
        raise ValueError('Canonical credit was removed from the distribution notice')
    copies = 0
    for path in package.glob('skills/*/resources/canonical/**/LICENSE*'):
        origin = path.relative_to(package).parts[4:]
        key = Path(*origin).as_posix()
        if path.is_symlink() or digest(path) != baseline['canonical_files'].get(key):
            raise ValueError('Resource license differs from its reviewed canonical origin')
        copies += 1
    if copies != 1:
        raise ValueError('Missing or unexpected resource license copies')
    result = subprocess.run([sys.executable, '-B', str(package / CHECKER), 'check', str(package),
                             '--exclude', 'examples/capabilities/G38/fixtures', '--json'],
                            capture_output=True, text=True, timeout=30)
    report = json.loads(result.stdout)
    findings = report['findings']
    note = None
    if host == 'antigravity':
        manifest = json.loads((package / 'plugin.json').read_text())
        if (set(manifest) != {'name', 'description'} or manifest['name'] != 'solaris-dev-shop'
                or not isinstance(manifest['description'], str) or not manifest['description'].strip()):
            raise ValueError('Unexpected Google native manifest')
        expected = [{'code': 'license_undeclared', 'detail': 'plugin.json license has no license value', 'path': 'plugin.json'}]
        if findings != expected or report['license'] != 'MIT' or set(report['declared_values']) != {'MIT', 'None'}:
            raise ValueError('Unexpected Google package provenance finding: ' + json.dumps(findings))
        note = 'The unmodified generic checker reports its missing-license-field policy for the strict Google root manifest. Google forbids that field; the real root MIT LICENSE and all canonical/resource notices remain verified. This finding is retained, not reported as a clean generic-checker result.'
    elif result.returncode != 0 or report['result'] != 'consistent' or findings:
        raise ValueError('Composite notice check failed: ' + result.stdout)
    return {'host': host, 'native_notice_consistency': True, 'canonical_checker_result': report['result'],
            'canonical_checker_exit': result.returncode, 'canonical_checker_findings': findings,
            'resource_license_copies_verified': copies, 'provider_format_note': note}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    packages = [('copilot', ROOT / 'copilot/plugin')] + [(host, ROOT / 'harnesses' / host)
                for host in ['deepseek', 'kilo', 'openclaw', 'antigravity']]
    reports = [verify(path, host) for host, path in packages]
    rejected = []
    if args.self_test:
        with tempfile.TemporaryDirectory(prefix='solaris-notice-controls-') as directory:
            trial = Path(directory) / 'package'
            shutil.copytree(ROOT / 'copilot/plugin', trial)
            verify(trial, 'copilot')
            def reject(label):
                try:
                    verify(trial, 'copilot')
                except ValueError:
                    rejected.append(label)
                else:
                    raise ValueError('False acceptance of ' + label)
            notice = trial / 'NOTICE.md'; original = notice.read_bytes()
            notice.write_bytes((trial / 'SOURCE-NOTICE.md').read_bytes())
            reject('unlisted resource license')
            notice.write_bytes(original)
            copy = next(trial.glob('skills/*/resources/canonical/**/LICENSE*')); content = copy.read_bytes()
            copy.write_bytes(content + b'\nchanged synthetic license\n')
            reject('changed resource license')
            copy.write_bytes(content)
            checker = trial / CHECKER; content = checker.read_bytes()
            checker.write_text("print('synthetic no-op')\n")
            reject('no-op checker')
            provenance = trial / 'SOLARIS-BUILD-SOURCE.json'; saved = provenance.read_bytes()
            metadata = json.loads(saved); metadata['canonical_files'][CHECKER] = digest(checker)
            provenance.write_text(json.dumps(metadata))
            reject('no-op checker with edited supplied manifest')
            checker.write_bytes(content); provenance.write_bytes(saved)
            verify(trial, 'copilot')
    print(json.dumps({'reports': reports, 'rejected_controls': rejected}, indent=2))


if __name__ == '__main__':
    main()
