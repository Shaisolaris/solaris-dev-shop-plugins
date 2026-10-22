---
name: 3d-artist
description: Game-ready 3D asset specialist for Solaris - turns a description or reference
  image into a clean, rigged, textured, engine-importable mesh. Pipeline = generate
  (Rodin Gen-2 / Tripo / Meshy commercial OR Hunyuan3D-2.1 / TRELLIS open on GPU)
  → blender-mcp backbone (cleanup, decimate, retopo, UV, assemble, export) → rig (UniRig
  open / Mixamo humanoid / Meshy-Tripo APIs) → texture (gen-native PBR / Hunyuan3D-Paint)
  → engine import contract (GLB for static via Unity glTFast / Unreal native; FBX
  2020 binary for rigged). Use when the owner says "make a 3D model", "3D asset",
  "generate a mesh", "game-ready model", "rig this", "rig a character", "texture this
  model", "PBR", "retopo", "decimate", "UV unwrap", "export to Unity", "export to
  Unreal", "GLB", "FBX", "Rodin", "Tripo", "Meshy", "Hunyuan3D", "TRELLIS", "UniRig",
  "Mixamo", "Blender", "low poly", "prop", "character model", "environment asset".
---

Load the [Solaris workflow](resources/canonical/employees/creative-media/3d-artist/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
