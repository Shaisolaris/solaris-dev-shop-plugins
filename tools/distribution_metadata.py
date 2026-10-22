"""Preserve canonical notices and CI snapshots as native distribution metadata."""
import hashlib
import json
from pathlib import Path


def add_resource_notices(root):
    root = Path(root)
    provenance_path = root / 'SOLARIS-BUILD-SOURCE.json'
    provenance = json.loads(provenance_path.read_text())
    canonical = provenance['canonical_files']
    if 'SOURCE-NOTICE.md' in canonical:
        raise ValueError('Apply notice derivation only to a fresh canonical-source layout')
    original = (root / 'NOTICE.md').read_bytes()
    if hashlib.sha256(original).hexdigest() != canonical['NOTICE.md']:
        raise ValueError('Canonical notice differs from its pinned source')
    aliases = []
    for path in sorted(root.rglob('*')):
        if not path.is_file() or not path.name.upper().startswith(('LICENSE', 'LICENCE', 'COPYING')):
            continue
        relative = path.relative_to(root).as_posix()
        if relative in canonical:
            continue
        parts = path.relative_to(root).parts
        if len(parts) < 5 or parts[0] != 'skills' or parts[2:4] != ('resources', 'canonical') or path.is_symlink():
            raise ValueError('Unmapped distribution license: ' + relative)
        origin = Path(*parts[4:]).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if origin not in canonical or canonical[origin] != digest:
            raise ValueError('Resource license does not match its declared canonical origin: ' + relative)
        aliases.append({'path': relative, 'canonical_origin': origin, 'sha256': digest})
    if not aliases:
        raise ValueError('Expected the contained resource license copy')
    (root / 'SOURCE-NOTICE.md').write_bytes(original)
    addition = '\n## Native distribution resource copies\n\n'
    addition += 'The original canonical notice is preserved in SOURCE-NOTICE.md. These documentation resource copies retain their credited source license bytes and terms; no additional relicensing is claimed.\n\n'
    for row in aliases:
        addition += '- `' + row['path'] + '` is a byte-identical copy of `' + row['canonical_origin'] + '` (SHA256 ' + row['sha256'] + ').\n'
    (root / 'NOTICE.md').write_bytes(original + addition.encode('utf-8'))
    canonical['SOURCE-NOTICE.md'] = canonical.pop('NOTICE.md')
    provenance['source_path_map']['NOTICE.md'] = 'SOURCE-NOTICE.md'
    record = {'canonical_notice': 'SOURCE-NOTICE.md', 'resource_license_aliases': aliases}
    provenance['distribution_notice'] = record
    provenance_path.write_text(json.dumps(provenance, indent=2) + '\n')
    return record


def relocate_source_ci(root):
    root = Path(root)
    provenance_path = root / 'SOLARIS-BUILD-SOURCE.json'
    provenance = json.loads(provenance_path.read_text())
    canonical = provenance['canonical_files']
    relocated = {}
    for name in sorted(list(canonical)):
        if not name.startswith('.github/'):
            continue
        source = root / name
        target_name = 'source-config/' + name
        target = root / target_name
        if source.is_symlink() or not source.is_file() or target.exists():
            raise ValueError('Unexpected source CI layout: ' + name)
        if hashlib.sha256(source.read_bytes()).hexdigest() != canonical[name]:
            raise ValueError('Source CI snapshot differs from its canonical digest: ' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        canonical[target_name] = canonical.pop(name)
        provenance['source_path_map'][name] = target_name
        relocated[name] = target_name
    if not relocated:
        raise ValueError('Expected canonical source CI snapshots')
    github = root / '.github'
    for directory in sorted(github.rglob('*'), reverse=True):
        if directory.is_dir():
            directory.rmdir()
    github.rmdir()
    provenance['relocated_repository_configuration'] = relocated
    provenance_path.write_text(json.dumps(provenance, indent=2) + '\n')
    return relocated
