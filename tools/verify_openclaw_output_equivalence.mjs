// Execute the actual old/new adapters with inert SDK and subprocess substitutes.
// No OpenClaw host, Python child, workflow, network or marketplace is started.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {execFileSync} from 'node:child_process';
import {promisify} from 'node:util';
import {fileURLToPath} from 'node:url';

const repository = process.argv[2];
assert(repository, 'Supply the native source repository');
const fidelityPath = process.argv[3];
assert(fidelityPath, 'Supply the reviewed resource-fidelity report');
const baseline = execFileSync('/usr/bin/git', ['-C', repository, 'show',
  'e02d8002d195f929e30fb5063bd04d4ed27190d6:tools/harness-assets/openclaw.mjs'],
  {encoding: 'utf8', env: {PATH: '/usr/bin:/bin', GIT_CONFIG_NOSYSTEM: '1',
                          GIT_CONFIG_GLOBAL: '/dev/null', GIT_CONFIG_SYSTEM: '/dev/null'}});
const candidate = fs.readFileSync(path.join(repository, 'tools/harness-assets/openclaw.mjs'), 'utf8');

async function invoke(source, words, options, response, executionFailure = false) {
  let output = '', action, plugin, descriptors;
  const calls = [], commands = [];
  const fakeExec = () => { throw new Error('The callback path must not execute'); };
  fakeExec[promisify.custom] = async (...args) => {
    calls.push(args);
    if (executionFailure) throw new Error('synthetic execution failure');
    return {stdout: JSON.stringify(response), stderr: ''};
  };
  const context = vm.createContext({Buffer, URL, process: {
    env: {PATH: '/usr/bin:/bin'}, stdout: {write(value) { output += value; }}
  }});
  const exports = {
    'node:child_process': {execFile: fakeExec}, 'node:util': {promisify},
    'node:url': {fileURLToPath},
    'openclaw/plugin-sdk/plugin-entry': {definePluginEntry(value) { return value; }}
  };
  const module = new vm.SourceTextModule(source, {context,
    initializeImportMeta(meta) { meta.url = 'file:///fixture/native/openclaw.mjs'; }});
  await module.link(async name => {
    assert(Object.hasOwn(exports, name), 'Unexpected import: ' + name);
    const values = exports[name];
    return new vm.SyntheticModule(Object.keys(values), function () {
      for (const [key, value] of Object.entries(values)) this.setExport(key, value);
    }, {context});
  });
  await module.evaluate({timeout: 1000});
  plugin = module.namespace.default;
  const chain = {
    command(name) { commands.push(name); return this; },
    description() { return this; }, argument() { return this; }, option() { return this; },
    action(callback) { action = callback; return this; }
  };
  plugin.register({registerCli(callback, metadata) { descriptors = metadata.descriptors; callback({program: chain}); }});
  let error = null;
  try { await action(words, options); } catch (failure) { error = failure.message; }
  for (const [executable, args, settings] of calls) {
    assert.equal(executable, 'python3');
    assert.deepEqual(Array.from(args).slice(0, 6),
      ['-B', '/fixture/skills/chief-of-staff/scripts/run.py', 'intake', '--json', '--', words.join(' ').trim()]);
    assert.equal(settings.timeout, 20000);
    assert.equal(settings.maxBuffer, 2 * 1024 * 1024);
    assert.deepEqual(Object.keys(settings.env).sort(), ['PATH', 'PYTHONDONTWRITEBYTECODE']);
    assert.equal(settings.env.PATH, '/usr/bin:/bin');
    assert.equal(settings.env.PYTHONDONTWRITEBYTECODE, '1');
  }
  return {output, error, calls: calls.length, commands,
    pluginId: plugin.id, machineOutput: [[], ['--json']].map(argv => descriptors[0].machineOutput({argv}))};
}

const cases = [];
for (const value of ['solaris.qa-engineer', '', 0, false, null, ['a', 'b'], {name: 'example'}]) {
  for (const json of [false, true]) {
    cases.push({id: 'OUTPUT-' + cases.length, words: ["literal '; $() request"], options: {json},
      response: {performed_work: false, decision: 'assign', assignment: {primary_capability: value}}});
  }
}
cases.push(
  {id: 'MISSING-ASSIGNMENT', words: ['help'], options: {}, response: {performed_work: false, decision: 'clarify'}},
  {id: 'UNEXPECTED-WORK', words: ['help'], options: {}, response: {performed_work: true}},
  {id: 'MISSING-WORK-GUARD', words: ['help'], options: {}, response: {}},
  {id: 'EMPTY-REQUEST', words: ['   '], options: {}, response: {performed_work: false}},
  {id: 'OVERSIZE-UTF8', words: ['é'.repeat(16385)], options: {}, response: {performed_work: false}},
  {id: 'EXECUTION-FAILURE', words: ['help'], options: {}, response: {}, executionFailure: true}
);
const results = [];
for (const item of cases) {
  const before = await invoke(baseline, item.words, item.options, item.response, item.executionFailure);
  const after = await invoke(candidate, item.words, item.options, item.response, item.executionFailure);
  assert.deepEqual(after, before, item.id);
  assert.deepEqual(after.commands, ['solaris', 'intake']);
  assert.equal(after.pluginId, 'solaris-dev-shop');
  assert.deepEqual(after.machineOutput, [false, true]);
  if (['EMPTY-REQUEST', 'OVERSIZE-UTF8'].includes(item.id)) {
    assert.equal(after.calls, 0); assert(after.error.includes('32768 UTF-8 bytes'));
  } else if (['UNEXPECTED-WORK', 'MISSING-WORK-GUARD'].includes(item.id)) {
    assert.equal(after.output, ''); assert(after.error.includes('unexpected execution result'));
  }
  results.push({caseId: item.id, baselineAndCandidateIdentical: true});
}
const fidelity = JSON.parse(fs.readFileSync(fidelityPath, 'utf8'));
assert.equal(fidelity.base, '8c5d1e21b8f4568e73cb58f81ff7ca27ca0d867f');
const changedCell = fidelity.tables.find(item => item.table === 'stacks/svelte.csv').reviewedCellChanges;
assert.equal(changedCell.length, 1);
const expressionBefore = changedCell[0].before;
const expressionAfter = changedCell[0].after;
assert.equal(expressionBefore, '{items.map(i => `<div>${i}</div>`)}');
assert.equal(expressionAfter, '{items.map(i => "<div>".concat(i, "</div>"))}');
const values = [
  ['string', 'label', '<div>label</div>'], ['number', 17, '<div>17</div>'],
  ['null', null, '<div>null</div>'], ['undefined', undefined, '<div>undefined</div>'],
  ['boolean', false, '<div>false</div>'], ['bigint', 12n, '<div>12</div>'],
  ['object', {toString() { return 'label'; }, valueOf() { return 7; }}, '<div>label</div>'],
  ['coercion-hint', {[Symbol.toPrimitive](hint) { return hint === 'string' ? 'name' : 19; }}, '<div>name</div>'],
  ['symbol-error', Symbol('label'), null]
];
const svelteResults = [];
for (const [id, value, expected] of values) {
  const executeExpression = expression => {
    try {
      return {result: new vm.Script('(' + expression.slice(1, -1) + ')').runInNewContext(
        {items: [value]}, {timeout: 100}), error: null};
    } catch (error) { return {result: null, error: error.message}; }
  };
  const before = executeExpression(expressionBefore), after = executeExpression(expressionAfter);
  assert.equal(JSON.stringify(after), JSON.stringify(before), id);
  if (expected === null) assert(after.error && after.error.includes('Symbol'));
  else { assert.equal(after.error, null); assert.equal(after.result[0], expected); }
  svelteResults.push({caseId: id, baselineAndCandidateIdentical: true});
}
console.log(JSON.stringify({cases: results, count: results.length, svelteResults,
  realSubprocessesOrNetworkStartedByAdapter: false, nativeMarketplaceAcceptance: false}, null, 2));
