#!/usr/bin/env python3
"""Verify the source and native-client boundaries of the two 0.68 exports.
Only explicit candidate clones and a NEW owned work directory are used.
No owner profile, key, provider account, model call, or publication is needed.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

CORE = 'c7c9b395795f488dd3c48122ff916970438b67e6'
NATIVE = '0ce43cd9a550a033a40b4e1f429a6c3c138802c2'
GEMINI = '9a50300f5b7ee39cc36a8edb1ac740ee22e1891d'
CLAUDE = '418e30c9530044196e5fdfcb8988f6bcb84879a8'
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')

def runtime_identity(path, key):
    plan = json.loads((Path(__file__).resolve().parents[1]/'EXPORT-068-REVIEW-PLAN.json').read_text())
    if sha(path.read_bytes()) != plan['runtime_identities'][key]['sha256']:
        raise ValueError('Unexpected runtime bytes: '+key)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def archive(root, revision):
    rows = {}
    with tarfile.open(fileobj=io.BytesIO(git(root, 'archive', revision))) as stream:
        for entry in stream:
            if entry.isdir():
                continue
            if not entry.isfile() or Path(entry.name).is_absolute() or '..' in Path(entry.name).parts:
                raise ValueError('Non-regular or escaping source member')
            rows[entry.name] = (stream.extractfile(entry).read(), bool(entry.mode & 0o111))
    return rows

def inventory(root):
    rows = {}
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if relative.parts[0] == '.git' or relative.as_posix() == '.gemini-extension-install.json':
            continue
        if path.is_symlink():
            raise ValueError('Symlink in installed/source payload')
        if path.is_file():
            rows[relative.as_posix()] = (path.read_bytes(), bool(path.stat().st_mode & 0o111))
    return rows

def assert_head(path, revision):
    if git(path, 'rev-parse', 'HEAD').decode().strip() != revision:
        raise ValueError('Wrong candidate revision')
    if git(path, 'status', '--porcelain'):
        raise ValueError('Candidate working tree must be clean')

def source_check(candidate, revision, core, kind):
    assert_head(candidate, revision)
    original = archive(core, CORE)
    record = json.loads((candidate/'SOLARIS-BUILD-SOURCE.json').read_text())
    mapping = {'README.md':'SOURCE-README.md'}
    mapping.update({name:'source-config/'+name for name in original if name.startswith('.github/')})
    if kind == 'gemini':
        mapping['NOTICE.md'] = 'SOURCE-NOTICE.md'
    expected = {mapping.get(name,name):sha(data) for name,(data,_) in original.items() if name != '.gitignore'}
    assert record['source_commit'] == CORE and record['canonical_files'] == expected
    assert record['source_path_map'] == mapping and len(expected) == 1201
    for name,(data,executable) in original.items():
        if name == '.gitignore':
            continue
        actual = candidate/mapping.get(name,name)
        assert not actual.is_symlink() and actual.read_bytes() == data, name
        assert bool(actual.stat().st_mode & 0o111) == executable, name
    index = json.loads((candidate/'native/skills.json').read_text())
    assert len(index) == len({row['name'] for row in index}) == 62
    for row in index:
        assert (candidate/'skills'/row['name']/'SKILL.md').is_file()
    if kind == 'gemini':
        manifest = json.loads((candidate/'gemini-extension.json').read_text())
        assert set(manifest) == {'name','version','description','contextFileName'}
        assert manifest['name'] == 'solaris-dev-shop' and manifest['version'] == '0.68.0'
        assert manifest['contextFileName'] == 'GEMINI.md'
    else:
        manifest = json.loads((candidate/'.claude-plugin/plugin.json').read_text())
        assert manifest['name'] == 'solaris-dev-shop' and manifest['version'] == '0.68.0'
        assert not manifest.get('mcpServers') and not manifest.get('hooks')
    assert not any((candidate/name).exists() for name in ['hooks/hooks.json','agents','policies'])
    return {'profile':kind,'revision':revision,'canonicalFilesAndModes':1201,'workflows':62}

def environment(work, node):
    home = work/'home'
    home.mkdir()
    gitconfig = work/'empty.gitconfig'
    gitconfig.touch()
    env = {k:os.environ[k] for k in ['TMPDIR','TEMP','TMP','SYSTEMROOT','SSL_CERT_FILE','SSL_CERT_DIR','LANG','LC_ALL'] if k in os.environ}
    env.update(HOME=str(home),GEMINI_CLI_HOME=str(home),CLAUDE_CONFIG_DIR=str(home/'claude'),
               PATH=str(Path(sys.executable).parent)+os.pathsep+str(node.parent)+os.pathsep+'/usr/bin:/bin',
               DO_NOT_TRACK='1',DISABLE_TELEMETRY='1',NO_COLOR='1',
               GEMINI_CLI_NO_RELAUNCH='true',CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1',
               GIT_TERMINAL_PROMPT='0',GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='credential.helper',GIT_CONFIG_VALUE_0='',
               GIT_CONFIG_GLOBAL=str(gitconfig),GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1')
    for key in ['CONFIG','DATA','CACHE','STATE']:
        directory = work/key.lower()
        directory.mkdir()
        env['XDG_'+key+'_HOME'] = str(directory)
    return env, home

def run(command, work, env, name, timeout=180):
    result = subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,timeout=timeout)
    (work/(name+'.stdout')).write_text(result.stdout)
    (work/(name+'.stderr')).write_text(result.stderr)
    if result.returncode:
        raise ValueError(name+' failed with exit '+str(result.returncode))
    return ANSI.sub('',result.stdout)

def smoke(native, installed, work):
    path = 'tools/verify_copilot_layout.py'
    assert (native/path).read_bytes() == git(native,'show',NATIVE+':'+path)
    sys.path.insert(0,str(native/'tools'))
    from verify_copilot_layout import smoke as actual_smoke
    sandbox = work/'helper-fixtures'
    sandbox.mkdir()
    return actual_smoke(installed,sandbox)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['source','gemini','claude'],required=True)
    parser.add_argument('--gemini',type=Path,required=True)
    parser.add_argument('--claude',type=Path,required=True)
    parser.add_argument('--core',type=Path,required=True)
    parser.add_argument('--native',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--node',type=Path)
    parser.add_argument('--gemini-cli',type=Path)
    parser.add_argument('--claude-cli',type=Path)
    args = parser.parse_args()
    for name in ['gemini','claude','core','native','work']:
        setattr(args,name,getattr(args,name).resolve())
    args.work.mkdir(parents=True,exist_ok=False)
    assert_head(args.core,CORE)
    reports = [source_check(args.gemini,GEMINI,args.core,'gemini'),
               source_check(args.claude,CLAUDE,args.core,'claude')]
    result = {'sourceChecks':reports,'mode':args.mode,'modelCommandsIssued':0,
              'modelUsageMetered':False,'modelClaimBasis':'Management/validation commands only; no inference operation or credential supplied',
              'ownerProfileModified':False,
              'providerApproval':False,'published':False}
    if args.mode == 'source':
        # Only source and offline coordinator checks; no vendor client/model.
        env,_ = environment(args.work,Path(sys.executable))
        for kind,candidate in [('gemini',args.gemini),('claude',args.claude)]:
            run([sys.executable,'-B',str(candidate/'control-plane/meta_control_plane.py'),'self-test'],
                args.work,env,kind+'-coordinator',60)
    elif args.mode == 'gemini':
        assert args.node and args.gemini_cli
        runtime_identity(args.node.resolve(),'node')
        runtime_identity(args.gemini_cli.resolve(),'gemini_entry')
        env,home = environment(args.work,args.node.resolve())
        cli = [str(args.node.resolve()),str(args.gemini_cli.resolve())]
        version = run(cli+['--version'],args.work,env,'version',45).strip()
        assert version == '0.65.0', version
        url = 'https://github.com/Shaisolaris/solaris-dev-shop-gemini'
        run(cli+['extensions','install',url,'--ref',GEMINI,'--consent'],args.work,env,'install',180)
        installed = home/'.gemini/extensions/solaris-dev-shop'
        metadata = json.loads((installed/'.gemini-extension-install.json').read_text())
        assert metadata['type'] == 'git' and metadata['ref'] == GEMINI
        assert metadata.get('autoUpdate',False) is False
        expected = archive(args.gemini,GEMINI)
        assert inventory(installed) == expected, 'Installed public Git bytes/modes differ'
        skills = run(cli+['skills','list','--all'],args.work,env,'skills',60)
        enabled = set(re.findall(r'^([^\s]+)\s+\[Enabled\](?:\s+\[Built-in\])?\s*$',skills,re.MULTILINE))
        names = {row['name'] for row in json.loads((installed/'native/skills.json').read_text())}
        assert names <= enabled and len(names) == 62
        result['native'] = {'host':'GeminiCLI0.65.0','pluginVersion':'0.68.0',
                            'publicGitRevision':GEMINI,'allFilesAndModes':len(expected),
                            'enabledNativeWorkflows':62,'normalSourceConsentFlag':True,
                            'forceFlagUsed':False,'autoUpdateFlagUsed':False,
                            'actualHelperOutcomes':smoke(args.native,installed,args.work)}
    else:
        assert args.claude_cli
        runtime_identity(args.claude_cli.resolve(),'claude_native')
        env,_ = environment(args.work,args.claude_cli.resolve())
        cli = [str(args.claude_cli.resolve())]
        version = run(cli+['--version'],args.work,env,'version',45).strip()
        assert version.startswith('2.1.306'),version
        text = run(cli+['plugin','validate',str(args.claude/'.claude-plugin/plugin.json'),
                        '--json','--profile','directory','--strict'],args.work,env,'strict-validation',60)
        strict = json.loads(text)
        assert strict['success'] is True and strict['strict'] is True
        assert not strict['manifest']['errors'] and not strict['manifest']['warnings']
        assert not strict['directory']['findings'] and not strict['directory']['incomplete'] and strict['directory']['failure'] is None
        result['native'] = {'host':'ClaudeCode2.1.306','validation':'strictdirectory','result':'PASS',
                            'marketplaceEligibilityEstablished':False}
    (args.work/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
