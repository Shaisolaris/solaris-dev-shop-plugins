#!/usr/bin/env python3
"""Rebuild the Copilot variant and exercise its entrypoints in owned fixtures.

Run verify_distribution.py first to bind the shared base to upstream and the
reviewed packager. This check adds the variant's complete byte/mode contract.
"""
from pathlib import Path
import argparse
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def members(root):
    result={}
    for file in root.rglob('*'):
        assert not file.is_symlink(), 'symlink: '+str(file.relative_to(root))
        if file.is_file():
            result[str(file.relative_to(root))]=(file.read_bytes(),bool(file.stat().st_mode&0o111))
    return result


def matches(package,expected):
    actual=members(package)
    assert actual.keys()==expected.keys(), 'missing or unexpected variant member'
    for name,item in expected.items():
        assert actual[name]==item, 'variant byte/mode mismatch: '+name


def smoke(package,work):
    def call(role,*args,code=0):
        run=subprocess.run([sys.executable,'-B',str(package/'skills'/role/'scripts/run.py'),*map(str,args)],
                           cwd=work,capture_output=True,text=True,timeout=20)
        assert run.returncode==code,(role,args,run.returncode,run.stdout,run.stderr)
        return run
    index=json.loads((package/'native/skills.json').read_text())
    assert len(index)==62
    for item in index:
        context=json.loads(call(item['name'],'--context').stdout)
        assert Path(context['plugin_root'])==package
        assert Path(context['canonical_folder'])==package/Path(item['canonical']).parent
    assigned=json.loads(call('chief-of-staff','intake','review this code','--json').stdout)
    assert assigned['decision']=='assign' and assigned['assignment']['primary_capability']=='solaris.code-reviewer'
    assert assigned['performed_work'] is False
    dataset=work/'dataset';dataset.mkdir()
    database=dataset/'app.db'
    with sqlite3.connect(database) as con:
        con.execute('CREATE TABLE items(id INTEGER PRIMARY KEY,value TEXT)')
        con.executemany('INSERT INTO items VALUES (?,?)',[(1,'alpha'),(2,'bravo')])
    (dataset/'neighbor.txt').write_bytes(b'keep')
    snapshot=work/'snapshot'
    snap=json.loads(call('database-administrator','sqlite_recovery.py','snapshot',dataset,'--out',snapshot,'--json').stdout)
    with sqlite3.connect(database) as con:
        con.execute("UPDATE items SET value='damaged'")
    call('database-administrator','sqlite_recovery.py','restore',dataset,'--snapshot',snapshot,'--confirm',snap['snapshot_id'])
    with sqlite3.connect(database) as con:
        assert con.execute('SELECT * FROM items ORDER BY id').fetchall()==[(1,'alpha'),(2,'bravo')]
    assert (dataset/'neighbor.txt').read_bytes()==b'keep'
    return {'context_workflows':62,'actual_assignment':'solaris.code-reviewer','actual_sqlite_rows_restored':2,'neighbor_unchanged':True}


def verify(self_test=False):
    package=ROOT/'copilot/plugin'
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory).resolve()
        generated=temp/'rebuilt'
        build=subprocess.run([sys.executable,str(ROOT/'tools/build_copilot_layout.py'),str(generated)],
                             capture_output=True,text=True,timeout=60)
        assert build.returncode==0,build.stderr
        expected=members(generated)
        assert len(expected)==1978
        matches(package,expected)
        result={'result':'PASS','payload_files':len(expected),'workflows':62,'new_employee_capabilities':0,'model_invocation':False}
        if self_test:
            unfinished=temp/'contained-input'
            prepared=subprocess.run([sys.executable,str(ROOT/'tools/build_copilot_layout.py'),str(unfinished),
                                     '--stage','contained-input'],capture_output=True,text=True,timeout=60)
            assert prepared.returncode==0,prepared.stderr
            try:
                matches(unfinished,expected)
            except AssertionError:
                pass
            else:
                raise AssertionError('Unfinished contained input falsely accepted as final distribution')
            copy=temp/'package';shutil.copytree(package,copy)
            work=temp/'work';work.mkdir()
            result['runtime']=smoke(copy,work)
            refused=['unfinished contained input rejected as final distribution']
            for target in ['../../control-plane/meta_control_plane.py','/tmp/not-a-helper.py']:
                bad=subprocess.run([sys.executable,'-B',str(copy/'skills/database-administrator/scripts/run.py'),target],capture_output=True,text=True,timeout=10)
                assert bad.returncode==2
                refused.append('helper escape: '+target)
            runtime=copy/'employees/infrastructure/database-administrator/sqlite_recovery.py'
            data=runtime.read_bytes()
            runtime.write_bytes(b"print('synthetic no-op sentinel')\n")
            bad=subprocess.run([sys.executable,'-B',str(copy/'skills/database-administrator/scripts/run.py'),'sqlite_recovery.py','--help'],capture_output=True,text=True,timeout=10)
            assert bad.returncode==2 and not bad.stdout and 'pinned source manifest' in bad.stderr
            refused.append('altered helper refused before execution')
            runtime.write_bytes(data)
            reference=copy/'skills/chief-of-staff/resources/canonical/chief-of-staff/SKILL.md'
            data=reference.read_bytes();reference.unlink()
            try:
                matches(copy,expected)
            except AssertionError:
                refused.append('missing contained workflow')
            reference.write_bytes(data)
            assert len(refused)==5
            matches(copy,expected)
            result['rejected_controls']=refused
        return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(verify(args.self_test),indent=2))
