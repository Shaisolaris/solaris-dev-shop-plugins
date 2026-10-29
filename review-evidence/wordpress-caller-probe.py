"""Read-only reproduction of the documented WordPress caller argument contract.

Runs only captured WP invocation expressions against an inert private fake wp.
No WordPress, Docker, database, network, public /tmp victim or owner account runs.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import tempfile

ROLE = pathlib.Path('employees/specialized/wordpress-master/diagnostics')
CASES = [
    ('WP-ARG-THEME', 'build-theme/SKILL.md', r'^\$WP option update blogname |^"\$\{WP\[@\]\}" option update blogname '),
    ('WP-ARG-CONTENT', 'build-content/SKILL.md', r'^\$WP option update show_on_front page|^"\$\{WP\[@\]\}" option update show_on_front page'),
    ('WP-ARG-MCP', 'build-mcp/SKILL.md', r'^\s*if ! (?:\$WP|"\$\{WP\[@\]\}") plugin activate mcp-adapter '),
    ('WP-ARG-VISUAL', 'build-visual/SKILL.md', r'^\$WP db export |^"\$\{WP\[@\]\}" db export '),
]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-root',type=pathlib.Path,required=True)
    parser.add_argument('--out',type=pathlib.Path,required=True)
    args=parser.parse_args()
    root=args.package_root.resolve(strict=True)
    scaffold=root/ROLE/'build-scaffold/SKILL.md'
    scaffold_bytes=scaffold.read_bytes()
    declarations=[line for line in scaffold_bytes.decode().splitlines() if line=='WP=(wp "--path=$BUILD_DIR")']
    if len(declarations)!=1:
        raise RuntimeError('Expected exactly the documented scaffold WP array declaration')
    snapshots={str(ROLE/'build-scaffold/SKILL.md'):digest(scaffold_bytes)}
    cases={}
    with tempfile.TemporaryDirectory(prefix='solaris-wp-caller-probe-') as temporary:
        workspace=pathlib.Path(temporary)
        bin_dir=workspace/'bin'
        bin_dir.mkdir(mode=0o700)
        fake_wp=bin_dir/'wp'
        fake_wp.write_text('#!/bin/sh\nset -eu\nprintf "%s\\0" "$@" > "$WP_PROBE_LOG"\n')
        fake_wp.chmod(0o700)
        for case_id,name,pattern in CASES:
            path=root/ROLE/name
            source=path.read_bytes()
            snapshots[str(ROLE/name)]=digest(source)
            matches=[(i+1,line.strip()) for i,line in enumerate(source.decode().splitlines()) if re.search(pattern,line)]
            if len(matches)!=1:
                raise RuntimeError(f'{case_id}: expected one documented call, found {len(matches)}')
            line,command=matches[0]
            if command.startswith('if ! '):
                if not command.endswith('; then'):
                    raise RuntimeError('Unexpected wrapper around the documented MCP call')
                command=command[len('if ! '):-len('; then')]
            if not (command.startswith('$WP ') or command.startswith('"${WP[@]}" ')):
                raise RuntimeError('Selected command is outside the approved WP-only scope')
            for suffix in ['plain-build', "build with spaces;literal-$()-'quote"]:
                build_dir=workspace/suffix
                build_dir.mkdir(exist_ok=True)
                log=workspace/'argv.nul'
                if log.exists():
                    log.unlink()
                env={'PATH':str(bin_dir)+':/usr/bin:/bin','LANG':'en_US.UTF-8','BUILD_DIR':str(build_dir),'SITE_TITLE':'Synthetic target title','WP_PROBE_LOG':str(log)}
                script='set -eu\n'+declarations[0]+'\n'+command+'\n'
                result=subprocess.run(['/bin/bash','--noprofile','--norc','-c',script],cwd=workspace,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
                argv=log.read_bytes().split(b'\0')[:-1] if log.exists() else []
                observed=[value.decode('utf-8') for value in argv]
                target_preserved=result.returncode==0 and observed and observed[0]=='--path='+str(build_dir)
                cases[case_id+('-PLAIN' if suffix=='plain-build' else '-LITERAL')]={
                    'passed':bool(target_preserved),'source':str(ROLE/name),'line':line,
                    'capturedCommand':command,'returncode':result.returncode,
                    'observedArguments':observed,'requiredFirstArgument':'--path='+str(build_dir),
                    'stderr':result.stderr.decode(),'usedOnlyInertPrivateWP':True,
                }
        for name,expected in snapshots.items():
            if digest((root/name).read_bytes())!=expected:
                raise RuntimeError('Source changed while the probe ran: '+name)
    report={'scope':'Private fake-WP argv probe of exact documented source calls; no real host business action','sourceSHA256':snapshots,'cases':cases,'errors':0,'sourceMutated':False,'modelCalls':0,'networkCalls':0,'realWPCalls':0}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    passed=all(case['passed'] for case in cases.values())
    print(json.dumps({'cases':len(cases),'passed':sum(c['passed'] for c in cases.values()),'out':str(args.out),'sourceMutated':False}))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
