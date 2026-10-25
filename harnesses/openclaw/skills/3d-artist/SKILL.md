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

Load the [canonical workflow](../../employees/creative-media/3d-artist/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
