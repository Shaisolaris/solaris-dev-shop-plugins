// Disposable native-host QA harness; never shipped as product source.
import assert from 'node:assert/strict';
import { access, writeFile } from 'node:fs/promises';
import solaris from './reviewed-entry.js';
export default async function(amp) {
 const registered=[];let registeredSkillCalls=0;
 await solaris(new Proxy(amp,{get(target,key){
  if(key==='registerSkill')return async definition=>{await target.registerSkill(definition);registeredSkillCalls++;};
  if(key==='registerTool')return definition=>{registered.push(definition);return target.registerTool(definition);};
  const value=Reflect.get(target,key);return typeof value==='function'?value.bind(target):value;
 }}));
 assert.equal(registeredSkillCalls,62);assert.equal(registered.length,1);const tool=registered[0];assert.equal(tool.name,'solaris_intake');
 const call=async input=>JSON.parse(await tool.execute(input,{}));
 const positive=await call({request:'review this code'});assert.equal(positive.assignment.primary_capability,'solaris.code-reviewer');assert.equal(positive.performed_work,false);
 const unclear=await call({request:'qxzv'});assert.equal(unclear.decision,'clarify');assert.equal(unclear.assignment,null);assert.equal(unclear.performed_work,false);
 const sentinel=new URL('./SHOULD-NOT-EXIST',import.meta.url);const literal=await call({request:'review this code; touch '+sentinel.pathname});assert.equal(literal.performed_work,false);await assert.rejects(access(sentinel));
 const option=await call({request:'--help review this code'});assert.equal(option.performed_work,false);
 let rejected=0;for(const input of [{request:'x'.repeat(32769)},{request:'💙'.repeat(8193)},{request:'review this code',command:'touch '+sentinel.pathname}]){await assert.rejects(()=>call(input));rejected++;}
 const after=await call({request:'review this code'});assert.equal(after.assignment.primary_capability,'solaris.code-reviewer');
 const report={host:'Official Amp CLI plugin process',scope:'Real registerSkill/registerTool APIs; registered execute callback invoked inside native process by disposable QA wrapper. No model/connected-thread dispatcher claim.',registeredSkillCalls,registeredNativeTools:1,actualAssignment:'solaris.code-reviewer',legitimateClarificationPreserved:true,literalShellSentinelAbsent:true,optionLikeInputLiteral:true,invalidInputControls:rejected,legitimateToolUsableAfterFailures:true,modelCalls:0,pass:true};
 await writeFile(new URL('./HOST-CALLBACK-PASS.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
}
