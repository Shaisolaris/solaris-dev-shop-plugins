import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const root = new URL('../', import.meta.url);

/** Register exactly the reviewed role index through Kilo's native V2 skill hook. */
export default {
  id: 'solaris.dev-shop',
  async setup(ctx) {
    const index = JSON.parse(await readFile(new URL('native/skills.json', root), 'utf8'));
    const skills = await Promise.all(index.map(async (skill) => ({
      name: skill.name,
      description: skill.description,
      location: fileURLToPath(new URL(skill.canonical, root)),
      content: (await readFile(new URL(skill.canonical, root), 'utf8'))
        .replace(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/, ''),
    })));
    await ctx.skill.transform((editor) => {
      for (const skill of skills) editor.source({ type: 'embedded', skill });
    });
  },
};
