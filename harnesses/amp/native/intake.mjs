import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';

const execute = promisify(execFile);
const helper = fileURLToPath(new URL('../skills/chief-of-staff/scripts/run.py', import.meta.url));

/** Route a bounded request locally. This never executes the assigned specialist. */
export async function intake(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)
      || Object.keys(input).some((key) => key !== 'request')
      || typeof input.request !== 'string' || !input.request.trim()
      || Buffer.byteLength(input.request, 'utf8') > 32768) {
    throw new Error('Expected only a nonempty request of at most 32768 UTF-8 bytes');
  }
  const { stdout } = await execute('python3', ['-B', helper, 'intake', '--json', '--', input.request], {
    timeout: 20000, maxBuffer: 1048576,
    env: { PATH: process.env.PATH ?? '', PYTHONDONTWRITEBYTECODE: '1' },
  });
  const result = JSON.parse(stdout);
  if (!result || typeof result !== 'object' || result.performed_work !== false || typeof result.decision !== 'string') {
    throw new Error('Coordinator returned an invalid routing result');
  }
  return result;
}

export const schema = {
  type: 'object', additionalProperties: false, required: ['request'],
  properties: { request: { type: 'string', minLength: 1, maxLength: 32768,
    description: 'Request to classify into one accountable Solaris assignment. No work is executed.' } },
};
