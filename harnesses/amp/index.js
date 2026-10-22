import { readFile } from 'node:fs/promises';
import { intake, schema } from './native/intake.mjs';

/** A directory plugin: Amp owns registration, namespacing and removal. */
export default async function (amp) {
  const skills = JSON.parse(await readFile(new URL('./native/skills.json', import.meta.url), 'utf8'));
  if (skills.length !== 62 || new Set(skills.map((skill) => skill.name)).size !== 62
      || skills.some((skill) => !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(skill.name))) {
    throw new Error('The reviewed Solaris roster must contain exactly 62 unique workflows');
  }
  for (const skill of skills) await amp.registerSkill({ path: 'skills/' + skill.name });
  amp.registerTool({
    name: 'solaris_intake',
    description: 'Classify a request through the pinned local Solaris coordinator. Returns an assignment; executes no specialist work.',
    inputSchema: schema,
    async execute(input) { return JSON.stringify(await intake(input)); },
  });
}
