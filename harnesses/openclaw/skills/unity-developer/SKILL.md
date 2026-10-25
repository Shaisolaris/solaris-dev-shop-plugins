---
name: unity-developer
description: ⚠️ ALWAYS load the Unity MCP operator references FIRST when ANY Unity
  work begins - `coplaydev-unity-mcp.md` (PRIMARY bridge) and `unity-mcp-operator.md`
  (IvanMurzak fallback + Tier-0 verify loop). Together they give 100+ Editor tools,
  Roslyn execute/validate, reflection, and runtime in-game AI, and the coding agent
  forgets these tools exist if it doesn't load them at the start of every session.
  Master skill for any Unity game project the owner is building. Use this whenever
  the session involves Unity, C# game scripts, GameObjects, scenes, prefabs, scene
  flow, UI/Canvas, shaders, physics, animation, input, builds for iOS/Android/PC/WebGL,
  testing on device, game design, player flow, MDA framework, screen navigation, game
  state logic, game feel, or anything involving a .unity file.
---

Load the [canonical workflow](../../employees/engineering/unity-developer/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
