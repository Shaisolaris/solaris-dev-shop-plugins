#!/usr/bin/env python3
"""Normal Factory management installs in new private homes; no model commands."""
import argparse
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

CATALOG = 'b9064234ba2eaae80bdf07a52045538dadf06457'
CATALOG_PATH = '.factory-plugin/marketplace.json'
SOURCES = {
    '066': ('e02d8002d195f929e30fb5063bd04d4ed27190d6', '0.66.0', 1979, 1200),
    '068': ('0ce43cd9a550a033a40b4e1f429a6c3c138802c2', '0.68.0', 1980, 1201),
}
CLI_SHA = 'f18812ff1017396664ce67f9754ad4732ac91b471004ccbc0315dff6dd3e59b5'
HELPER_SHA = 'c6df557082a861b90c30a8ddd9e372f08a10532153d3145111654817f9563d2f'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args, env=None):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env)


def expected_profile(native, ref, version, count, canonical_count):
    rows = {}
    with tarfile.open(fileobj=io.BytesIO(git(native, 'archive', ref + ':copilot/plugin'))) as archive:
        for item in archive:
            if item.isdir():
                continue
            assert item.isfile() and not Path(item.name).is_absolute() and '..' not in Path(item.name).parts
            rows[item.name] = (archive.extractfile(item).read(), bool(item.mode & 0o111))
    assert len(rows) == count
    assert json.loads(rows['plugin.json'][0])['version'] == version
    provenance = json.loads(rows['SOLARIS-BUILD-SOURCE.json'][0])
    assert len(provenance['canonical_files']) == canonical_count
    for name, digest in provenance['canonical_files'].items():
        assert sha(rows[name][0]) == digest, name
    names = {item['name'] for item in json.loads(rows['native/skills.json'][0])}
    assert len(names) == 62
    return rows, names


def inventory(root):
    rows = {}
    for path in root.rglob('*'):
        if '.git' in path.relative_to(root).parts:
            continue
        assert not path.is_symlink(), str(path)
        if path.is_file():
            rows[path.relative_to(root).as_posix()] = (path.read_bytes(), bool(path.stat().st_mode & 0o111))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['native', 'catalog', 'cli', 'work']:
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    native, catalog, cli, work = (getattr(args, name).resolve() for name in ['native', 'catalog', 'cli', 'work'])
    assert sha(cli.read_bytes()) == CLI_SHA
    original = json.loads(git(catalog, 'show', CATALOG + ':' + CATALOG_PATH))
    entries = [item for item in original['plugins'] if item['name'] == 'solaris-dev-shop']
    assert len(entries) == 1
    entry = entries[0]
    assert entry['source'] == {
        'source': 'git-subdir',
        'url': 'https://github.com/Shaisolaris/solaris-dev-shop-plugins',
        'path': 'copilot/plugin',
        'sha': SOURCES['066'][0],
    }, entry['source']
    assert 'version' not in entry
    work.mkdir(parents=True, exist_ok=False)
    outcomes = []
    for lane, (ref, version, count, canonical_count) in SOURCES.items():
        expected, skill_names = expected_profile(native, ref, version, count, canonical_count)
        native_expected = dict(expected)
        assert '.claude-plugin/plugin.json' in native_expected
        assert '.factory-plugin/plugin.json' not in native_expected
        native_expected['.factory-plugin/plugin.json'] = native_expected.pop('.claude-plugin/plugin.json')
        state = work / lane
        state.mkdir()
        home = state / 'home'
        home.mkdir()
        temporary = state / 'tmp'
        temporary.mkdir()
        gitconfig = state / 'empty.gitconfig'
        gitconfig.touch()
        env = {
            'HOME': str(home), 'FACTORY_HOME_OVERRIDE': str(home), 'TMPDIR': str(temporary),
            'XDG_CONFIG_HOME': str(home / 'config'), 'XDG_CACHE_HOME': str(home / 'cache'),
            'XDG_DATA_HOME': str(home / 'data'), 'PATH': str(Path(sys.executable).parent) + ':/usr/bin:/bin',
            'DO_NOT_TRACK': '1', 'FACTORY_DISABLE_TELEMETRY': '1', 'FACTORY_NO_AUTOUPDATE': '1',
            'PYTHONDONTWRITEBYTECODE': '1', 'NO_COLOR': '1', 'TERM': 'dumb', 'LANG': 'en_US.UTF-8',
            'GIT_TERMINAL_PROMPT': '0', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': str(gitconfig),
            'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'credential.helper', 'GIT_CONFIG_VALUE_0': '',
        }
        fixture_name = 'solaris-factory-' + lane + '-qa'
        fixture = state / fixture_name
        (fixture / '.factory-plugin').mkdir(parents=True)
        fixture_entry = copy.deepcopy(entry)
        fixture_entry['source']['sha'] = ref
        manifest = {
            'name': fixture_name, 'description': 'Private native QA fixture; no marketplace approval.',
            'owner': {'name': 'Solaris QA fixture'}, 'plugins': [fixture_entry],
        }
        (fixture / CATALOG_PATH).write_text(json.dumps(manifest, indent=2) + '\n')
        git(fixture, 'init', '-q', '-b', 'fixture', env=env)
        git(fixture, 'add', CATALOG_PATH, env=env)
        git(fixture, '-c', 'user.name=Solaris QA fixture', '-c', 'user.email=fixture@example.invalid',
            'commit', '-q', '-m', 'Private catalog fixture', env=env)

        def run(label, arguments):
            result = subprocess.run([str(cli), *arguments], cwd=state, env=env,
                                    capture_output=True, text=True, timeout=180)
            (state / (label + '.stdout')).write_text(result.stdout)
            (state / (label + '.stderr')).write_text(result.stderr)
            assert result.returncode == 0, label + ': ' + result.stderr[-4000:]
            return result.stdout

        assert re.search(r'(?<![\d.])0\.247\.0(?![\d.])', run('version', ['--version']))
        run('add', ['plugin', 'marketplace', 'add', fixture.as_uri()])
        run('install', ['plugin', 'install', 'solaris-dev-shop@' + fixture_name])
        listed = run('list', ['plugin', 'list'])
        enabled = listed.split('Disabled:')[0]
        assert 'Enabled:' in enabled and 'solaris-dev-shop@' + fixture_name in enabled, listed
        cache = home / '.factory/plugins/cache'
        installed = [p.parent for p in cache.rglob('COPILOT-LAYOUT.json')]
        assert len(installed) == 1, installed
        root = installed[0]
        assert inventory(root) == native_expected, 'Installed source files/modes differ beyond the exact native manifest relocation: ' + ref
        assert {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')} == skill_names
        outcome = {'source': ref, 'version': version, 'matchingFilesAndModes': count,
                   'canonicalFiles': canonical_count, 'registeredEnabledPlugin': True,
                   'nativeSkillEntryFiles': 62, 'modelCommandsIssued': 0,
                   'directPathMatches': count - 1,
                   'nativeManifestRelocation': {'.claude-plugin/plugin.json': '.factory-plugin/plugin.json'},
                   'ownerConfigurationPassed': False, 'publicListingAccepted': False}
        if lane == '068':
            helper = native / 'tools/verify_copilot_layout.py'
            assert sha(helper.read_bytes()) == HELPER_SHA
            assert helper.read_bytes() == git(native, 'show', ref + ':tools/verify_copilot_layout.py')
            sys.path.insert(0, str(helper.parent))
            saved_environment = dict(os.environ)
            try:
                os.environ.clear()
                os.environ.update(env)
                from verify_copilot_layout import smoke
                fixtures = state / 'recovery-fixtures'
                fixtures.mkdir()
                outcome['actualHelperOutcomes'] = smoke(root, fixtures)
            finally:
                os.environ.clear()
                os.environ.update(saved_environment)
        assert inventory(root) == native_expected, 'Installed source changed during checks'
        outcomes.append(outcome)
    assert sha(cli.read_bytes()) == CLI_SHA
    report = {'factoryHost': 'Droid0.247.0', 'fixtureTransport': 'owned local Git catalog',
              'productTransport': 'normal public GitHub git-subdir source at exact SHA',
              'outcomes': outcomes, 'upstreamSubmissionChanged': False,
              'productionActivation': False, 'releaseAllowed': False, 'pass': True}
    (work / 'RESULT.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
