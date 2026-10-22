import { readFileSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const root = new URL('../', import.meta.url);
const index = JSON.parse(readFileSync(new URL('native/skills.json', root), 'utf8'));
const invocation = Object.freeze({ modelInvocable: true, userInvocable: true });

/** Native Cordis skill provider; it reads only this installed bundle's resources. */
export const name = 'solaris-dev-shop';
export const inject = ['skills'];

export function apply(ctx) {
  const candidates = index.map((skill) => {
    const path = fileURLToPath(new URL(skill.canonical, root));
    return { name: skill.name, description: skill.description, invocation,
      path, provider: name, source: 'bundled', rank: 600,
      resourceBase: { kind: 'directory', path: dirname(path) }, locator: path };
  });
  ctx.skills.registerProvider(() => ({
    name,
    async list() { return candidates; },
    async get(candidate) {
      const owned = candidates.find((row) => row.name === candidate.name);
      if (!owned) return undefined;
      const text = await readFile(owned.locator, 'utf8');
      const content = text.replace(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/, '');
      const { rank, locator, ...summary } = owned;
      return { ...summary, content };
    },
  }));
}
