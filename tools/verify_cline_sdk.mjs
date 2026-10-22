import assert from 'node:assert/strict';
import { readFile, writeFile, access } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [modules,plugin,skillsFile,cwd]=process.argv.slice(2).map(value=>path.resolve(value));
assert.equal(JSON.parse(await readFile(path.join(modules,'@cline/sdk/package.json'),'utf8')).version,'0.0.95');
const sdk=await import(pathToFileURL(path.join(modules,'@cline/sdk/dist/index.js')).href);
const shared=await import(pathToFileURL(path.join(modules,'@cline/shared/dist/index.js')).href);
const packageRoot=path.dirname(plugin);
const index=JSON.parse(await readFile(path.join(packageRoot,'native/skills.json'),'utf8'));
const rows=JSON.parse(await readFile(skillsFile,'utf8')).filter(x=>x.path.startsWith(packageRoot+path.sep));
assert.equal(rows.length,62);assert.equal(new Set(rows.map(x=>x.name)).size,62);
for(const item of index){const row=rows.find(x=>x.name===item.name);assert(row);const skillFile=path.join(packageRoot,'skills',item.name,'SKILL.md');const expected=sdk.parseSkillConfigFromMarkdown(await readFile(skillFile,'utf8'),item.name);assert.equal(row.path,skillFile);assert.equal(row.description,expected.description);assert.equal(row.instructions,expected.instructions);}

const registry=new sdk.PluginRegistry();
const loaded=await sdk.resolveAndLoadAgentPlugins({pluginPaths:[plugin],cwd,workspacePath:cwd,registry,hookErrorMode:'throw'});
assert.equal(loaded.issues.length,0);assert.equal(loaded.failures.length,0);assert.equal(loaded.extensions.length,1);
try{
 const contributions=new shared.ContributionRegistry({extensions:loaded.extensions,setupContext:{cwd}});
 await contributions.initialize();const tools=contributions.getRegisteredTools();assert.equal(tools.length,1);const tool=tools[0];assert.equal(tool.name,'solaris_intake');
 const context={agentId:'solaris-native-qa',iteration:0,cwd};
 const positive=await tool.execute({request:'review this code'},context);assert.equal(positive.assignment.primary_capability,'solaris.code-reviewer');assert.equal(positive.performed_work,false);
 const unclear=await tool.execute({request:'qxzv'},context);assert.equal(unclear.decision,'clarify');assert.equal(unclear.assignment,null);assert.equal(unclear.performed_work,false);
 const sentinel=path.join(cwd,'SHOULD-NOT-EXIST');const literal=await tool.execute({request:'review this code; touch '+sentinel},context);assert.equal(literal.performed_work,false);await assert.rejects(access(sentinel));
 const option=await tool.execute({request:'--help review this code'},context);assert.equal(option.performed_work,false);
 let rejected=0;for(const input of [{request:'x'.repeat(32769)},{request:'💙'.repeat(8193)},{request:'review code',command:'touch '+sentinel}]){await assert.rejects(()=>tool.execute(input,context));rejected++;}
 const after=await tool.execute({request:'review this code'},context);assert.equal(after.assignment.primary_capability,'solaris.code-reviewer');
 const report={host:'Cline CLI3.0.73 and real SDK0.0.95 worker+ContributionRegistry',nativeOwnedSkillBodiesDescriptionsPaths:62,registeredNativeTools:1,actualToolAssignment:'solaris.code-reviewer',legitimateClarificationPreserved:true,literalShellSentinelAbsent:true,optionLikeInputLiteral:true,invalidInputControls:rejected,legitimateToolUsableAfterFailures:true,modelCalls:0,pass:true};
 console.log(JSON.stringify(report,null,2));
}finally{await loaded.shutdown?.();}
