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

Load the [Solaris workflow](resources/canonical/employees/engineering/unity-developer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
