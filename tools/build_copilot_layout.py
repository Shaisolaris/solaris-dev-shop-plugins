"""Build a Copilot layout with contained documentation and real local entrypoints.

The shared pinned runtime is retained once. Mirrors are packaging resources,
not new role capabilities. No source implementation or release version changes.
"""
from pathlib import Path
import argparse
import sys
import hashlib
import json
import re
import shutil
from urllib.parse import unquote, urlsplit
from distribution_metadata import add_resource_notices, relocate_source_ci

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'plugin'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path)
parser.add_argument('--stage', choices=['distribution', 'contained-input'], default='distribution',
                    help='contained-input prepares an unpublished source snapshot; final packages always derive notices and inert CI metadata')
ARGS = parser.parse_args()
OUT = ARGS.output.resolve()

RUNNER = '''#!/usr/bin/env python3
"""Invoke this workflow's pinned shared runtime; host permissions still apply."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

CANONICAL = __CANONICAL__
ROOT = Path(__file__).resolve().parents[3]
ROLE = ROOT / Path(CANONICAL).parent
PROVENANCE = ROOT / 'SOLARIS-BUILD-SOURCE.json'

def main():
    source = json.loads(PROVENANCE.read_text())
    canonical = ROOT / CANONICAL
    if hashlib.sha256(canonical.read_bytes()).hexdigest() != source['canonical_files'][CANONICAL]:
        raise ValueError('Canonical workflow differs from its pinned source manifest')
    if sys.argv[1:] == ['--context']:
        print(json.dumps({'plugin_root': str(ROOT), 'canonical_folder': str(ROLE),
                          'source_commit': source['source_commit']}))
        return 0
    if CANONICAL == 'chief-of-staff/SKILL.md':
        target = ROOT / 'control-plane/meta_control_plane.py'
        args = sys.argv[1:]
        cwd = ROOT
    else:
        if len(sys.argv) < 2:
            raise ValueError('Supply a role-relative Python helper and its arguments, or --context')
        relative = Path(sys.argv[1])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('The helper must stay inside this canonical role folder')
        target = (ROLE / relative).resolve()
        if not target.is_relative_to(ROLE.resolve()):
            raise ValueError('The helper resolves outside this canonical role folder')
        args = sys.argv[2:]
        cwd = ROLE
    if target.suffix != '.py' or not target.is_file():
        raise ValueError('Expected an existing Python helper')
    key = str(target.relative_to(ROOT))
    expected = source['canonical_files'].get(key)
    if not expected or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
        raise ValueError('Helper differs from its pinned source manifest')
    return subprocess.run([sys.executable, '-B', str(target), *args], cwd=cwd).returncode

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
'''


def build():
    assert not OUT.exists(), 'Do not overwrite an existing candidate.'
    shutil.copytree(BASE, OUT, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    canonical = json.loads((BASE/'SOLARIS-BUILD-SOURCE.json').read_text())
    assert canonical['source_commit'] == '1f06f27288ba47143574742bd340228ea492962c', 'Review a new upstream revision before changing this pin.'
    index = json.loads((BASE/'native/skills.json').read_text())
    records = {}
    original_missing = []
    for skill in index:
        name = skill['name']
        original_path = skill['canonical']
        role_dir = Path(original_path).parent
        folder = OUT/'skills'/name
        mirror = folder/'resources/canonical'
        pending = [key for key in canonical['canonical_files'] if Path(key).is_relative_to(role_dir)]
        copied = {}
        while pending:
            key = pending.pop()
            if key in copied:
                continue
            f = BASE/key
            if not f.is_file() or key not in canonical['canonical_files']:
                continue
            data = f.read_bytes()
            expected = canonical['canonical_files'][key]
            assert hashlib.sha256(data).hexdigest() == expected
            target = mirror/key
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(f,target)
            copied[key] = expected
            if f.suffix.lower() != '.md':
                continue
            for raw in re.findall(r'\]\(([^)]+)\)',data.decode('utf-8')):
                link = urlsplit(raw)
                if link.scheme or not link.path:
                    continue
                dest = (f.parent/unquote(link.path)).resolve()
                if not dest.is_relative_to(BASE.resolve()):
                    original_missing.append({'skill':name,'from':key,'reference':raw,'reason':'outside original package'})
                    continue
                rel = str(dest.relative_to(BASE))
                if rel == 'README.md':
                    # Preserve the same actual packaged README target used by the canonical file.
                    # It is not canonical source and must not be silently copied as one.
                    original_missing.append({'skill':name,'from':key,'reference':raw,'reason':'generated README target requires explicit mirror handling'})
                    continue
                if rel in canonical['canonical_files']:
                    pending.append(rel)
                elif dest.is_dir():
                    pending.extend(x for x in canonical['canonical_files'] if Path(x).is_relative_to(rel))
                else:
                    original_missing.append({'skill':name,'from':key,'reference':raw,'reason':'not an existing canonical target'})
        script = folder/'scripts/run.py'
        script.parent.mkdir(exist_ok=True)
        script.write_text(RUNNER.replace('__CANONICAL__',repr(original_path)))
        script.chmod(0o755)
        f = folder/'SKILL.md'
        front = f.read_text().split('---',2)[1]
        body = f'Load the [Solaris workflow](resources/canonical/{original_path}) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.\n\n'
        if name == 'chief-of-staff':
            body += 'Use the local [routing entrypoint](scripts/run.py) for canonical coordinator commands, such as `python <resolved-entrypoint> intake "review this code" --json`. Resolve the entrypoint relative to this skill file; it locates the pinned shared engine and supplies its correct working directory.\n\n'
        else:
            body += 'For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.\n\n'
        body += 'The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.\n'
        f.write_text('---'+front+'---\n\n'+body)
        records[name]={'canonical_workflow':original_path,'mirrored_canonical_files':copied,
                       'entrypoint_sha256':hashlib.sha256(script.read_bytes()).hexdigest()}
    ignored_examples = set([('employees/engineering/unreal-developer/unreal-genai-asset-gen.md', 'const FString& Response, const FString& Error, bool bSuccess'), ('employees/specialized/wordpress-master/diagnostics/build-scrape/SKILL.md', '[^\\"\\\\\'>{]+'), ('employees/specialized/wordpress-master/diagnostics/build-scrape/SKILL.md', '{source_url}'), ('employees/specialized/wordpress-master/diagnostics/build-scrape/SKILL.md', '{url}')])
    assert all((x['from'], x['reference']) in ignored_examples for x in original_missing), original_missing
    report={'prototype':False,'source_native_commit':'2ca1ffa5597981a1effbbcd43aefdc82ce03d124',
            'source_core_commit':canonical['source_commit'],'version':canonical['native_version'],
            'metadata_stage':ARGS.stage,
            'workflow_count':len(records),'new_role_capabilities':0,'mirrors':records,
            'excluded_code_example_patterns':original_missing}
    (OUT/'README.md').write_text('''# Solaris Dev Shop for GitHub Copilot

This distribution preserves the 61 specialist workflows and coordinating intake workflow. Each discoverable skill contains its canonical workflow/reference mirror and a local entrypoint; the pinned runtime is shared at the plugin root. Mirrors satisfy the marketplace resource layout and add no new employee capabilities. The exact version and source are recorded in SOLARIS-BUILD-SOURCE.json.

Use the local skill entrypoint for Python helpers. It preserves the original canonical working directory and refuses a helper that differs from its source manifest. Host permissions, approvals, tools and documented runtime requirements still apply. This is not a security sandbox.

The source revision, mirror hashes and local entrypoint hashes are recorded in SOLARIS-BUILD-SOURCE.json and COPILOT-LAYOUT.json. See the repository COPILOT-SUBMISSION.md for validation and marketplace status. No model activation or marketplace approval is implied.
''')
    if ARGS.stage == 'distribution':
        report['distribution_notice'] = add_resource_notices(OUT)
        report['relocated_repository_configuration'] = relocate_source_ci(OUT)
    else:
        report['publication_ready'] = False
        report['required_before_publication'] = 'Derive resource notices and relocate canonical CI snapshots exactly once in each final profile.'
    (OUT/'COPILOT-LAYOUT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'workflows':len(records),'mirror_files':sum(len(x['mirrored_canonical_files']) for x in records.values()),
                      'unresolved_original_references':len(original_missing),'prototype':False}))


if __name__ == '__main__':
    build()
