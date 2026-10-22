#!/usr/bin/env python3
"""Invoke this workflow's pinned shared runtime; host permissions still apply."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

CANONICAL = 'employees/engineering/llm-agent-designer/SKILL.md'
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
