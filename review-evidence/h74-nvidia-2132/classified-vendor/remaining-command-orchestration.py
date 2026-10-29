"""Finish ONLY the six already-approved, unperformed official CLI commands.

These are vendor results only; final exact occurrence reconciliation is separate.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import importlib.util,json,subprocess,time
F=Path(__file__).resolve().parent
R=Path('/tmp/solaris-nvidia-remediation-20261028')
spec=importlib.util.spec_from_file_location('classification',R/'review-evidence/nvidia_h74_exact_classification.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
S=F/'nvidia-2132-h74-scopes';OUT=F/'nvidia-2132-h74-classified';candidate=F/'release-070-h74/openclaw';runtime=Path('/tmp/solaris-skillspector-2132-20261029').resolve();parser=Path('/tmp/solaris-skillspector-static-20261028/bin').resolve();scanner=C.DRIVER.verify_runtime(runtime)
assert C.sha(parser/'shfmt')==C.DRIVER.SHFMT_SHA256
manifest=C.read(S/'partition.json');frozen=C.DRIVER.validate_git(candidate,R,C.REVISION);assert manifest['files']==frozen and len(frozen)==1348
review_path=F/'H74-EXACT-CLASSIFICATION-SIDECAR.json';review=C.read(review_path);digest=C.sha(review_path);assert review['source_revision']==C.REVISION and review['scanner_version']==C.VERSION
keys=set()
for scope in manifest['scopes']:
 raw_path=S/'scopes'/scope['id']/'raw-report.json';exact=subprocess.check_output(['git','-C',str(R),'show',C.RAW_EVIDENCE+':review-evidence/h74-nvidia-2132/'+scope['id']+'-raw-report.json']);assert raw_path.read_bytes()==exact
 raw=C.read(raw_path);C.assert_complete(raw,raw_path.parent/'input',scope['files'])
 for issue in raw['issues']:
  key=C.review_key(issue);row=review['findings'][key];assert row['disposition']=='contextual-false-positive' and row['finding_id']==issue['finding_id'] and row['source_sha256']==C.sha_component(candidate,issue['location']['file']) and len(row['reason'])>=32;assert key not in keys;keys.add(key)
assert set(review['findings'])==keys and len(keys)==846
reason=('Exact contextual false positives individually reviewed in sidecar SHA256 '+digest+'; source '+C.REVISION+'; original findings '+C.RAW_EVIDENCE+'. Reasons and source hashes are recorded per review key. No new findings or coverage gaps accepted.')
def run_scope(scope):
 folder=OUT/scope['id'];folder.mkdir(mode=0o700);home=folder/'home';home.mkdir(mode=0o700);root=(S/'scopes'/scope['id']/'input').resolve();commands=[]
 env={'PATH':str(scanner.parent)+':'+str(parser)+':/usr/bin:/bin','HOME':str(home),'XDG_CACHE_HOME':str(home/'cache'),'LANG':'en_US.UTF-8','PYTHONUNBUFFERED':'1','SKILLSPECTOR_BUILD_REVISION':C.DRIVER.SCANNER_RELEASE}
 def run(label,args):
  command=[str(scanner),*args];start=time.monotonic()
  with (folder/(label+'.stdout.log')).open('x') as out,(folder/(label+'.stderr.log')).open('x') as err:r=subprocess.run(command,cwd=folder,env=env,stdout=out,stderr=err,timeout=720)
  commands.append({'label':label,'command':command,'exit':r.returncode,'seconds':round(time.monotonic()-start,3)});(folder/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');assert r.returncode==0
 baseline=folder/'official-baseline.json';raw=C.read(S/'scopes'/scope['id']/'raw-report.json');run('generate',['baseline',str(root),'--no-llm','--output',str(baseline),'--reason',reason]);assert 'Scan analysis is incomplete' not in (folder/'generate.stderr.log').read_text();C.assert_baseline(C.read(baseline),raw['issues'],reason);before=C.sha(baseline)
 report_path=folder/'classified-report.json';run('classified',['scan',str(root),'--output',str(report_path),'--baseline',str(baseline),'--show-suppressed',*C.DRIVER.STRICT_FLAGS]);report=C.read(report_path);C.assert_complete(report,root,scope['files']);assert report['risk_assessment']['score']==0 and report['risk_assessment']['recommendation']=='SAFE' and report['issues']==[] and C.sha(baseline)==before
 receipt={'scope':scope['id'],'nativeExit':0,'nativeComplete':True,'nativeCoverage':100,'nativeRecommendation':'SAFE','nativeScore':0,'nativeActiveFindings':0,'requiresFinalOccurrenceReconciliation':True,'releaseClearance':False,'reportSha256':C.sha(report_path),'baselineSha256':before};(folder/'VENDOR-ONLY-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
remaining=[s for s in manifest['scopes'] if s['id'] in ('scope-006','scope-007','scope-008')];assert len(remaining)==3 and all(not (OUT/s['id']).exists() for s in remaining)
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run_scope,remaining))
C.DRIVER.verify_runtime(runtime);assert C.DRIVER.validate_git(candidate,R,C.REVISION)==frozen and C.sha(review_path)==digest and C.sha(parser/'shfmt')==C.DRIVER.SHFMT_SHA256
(F/'FINISHED-APPROVED-COMMANDS-RECEIPT.json').write_text(json.dumps({'results':results,'newVendorCommands':6,'repeatedCompletedCommands':0,'sourceAndVendorUnchanged':True,'releaseClearance':False},indent=2)+'\n');print(json.dumps(results,indent=2))
