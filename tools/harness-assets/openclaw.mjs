import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';

const execute = promisify(execFile);
const helper = fileURLToPath(new URL('../skills/chief-of-staff/scripts/run.py', import.meta.url));
const descriptor = { name: 'solaris', description: 'Route a request through the pinned Solaris coordinator', hasSubcommands: true };

export default definePluginEntry({
  id: 'solaris-dev-shop',
  name: 'Solaris Dev Shop',
  description: '61 specialist workflows, a coordinator and native deterministic intake',
  register(api) {
    api.registerCli(({ program }) => {
      program.command('solaris').description(descriptor.description)
        .command('intake').description('Return a bounded assignment; does not execute specialist work')
        .argument('<request...>', 'Request to route')
        .option('--json', 'Print the complete structured assignment')
        .action(async (words, options) => {
          const request = words.join(' ').trim();
          if (!request || Buffer.byteLength(request, 'utf8') > 32768) throw new Error('Supply between 1 and 32768 UTF-8 bytes of request text');
          const { stdout } = await execute('python3', ['-B', helper, 'intake', '--json', '--', request], {
            timeout: 20000,
            maxBuffer: 2 * 1024 * 1024,
            windowsHide: true,
            env: { PATH: process.env.PATH ?? '/usr/bin:/bin', PYTHONDONTWRITEBYTECODE: '1' },
          });
          const result = JSON.parse(stdout);
          if (result.performed_work !== false) throw new Error('Coordinator returned an unexpected execution result');
          process.stdout.write((options.json ? JSON.stringify(result) : ''.concat(result.decision, ': ', result.assignment?.primary_capability ?? 'See the structured intake result')) + '\n');
        });
    }, { descriptors: [{ ...descriptor, machineOutput: ({ argv }) => argv.includes('--json') }] });
  },
});
