import { Plugin } from "@opencode/plugin";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
const root = new URL("../", import.meta.url);
export default Plugin.define({
  id: "solaris.dev-shop",
  async setup(ctx) {
    const index = JSON.parse(await readFile(new URL("native/skills.json", root), "utf8"));
    const skills = await Promise.all(index.map(async (skill) => {
      const path = fileURLToPath(new URL(skill.canonical, root));
      return { id: "solaris." + skill.name, name: skill.name,
        description: skill.description, path, content: await readFile(path, "utf8") };
    }));
    await ctx.skill.transform((editor) => { for (const skill of skills) editor.add(skill); });
  },
});
