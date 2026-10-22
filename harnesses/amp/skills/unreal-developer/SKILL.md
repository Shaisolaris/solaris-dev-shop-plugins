---
name: unreal-developer
description: ⚠️ ALWAYS load `unreal-mcp-operator.md` FIRST when ANY Unreal work begins
  - it is the canonical ChiR24/Unreal_mcp reference (23 broad action-dispatch tools
  across asset/blueprint(+UMG)/actor/editor/level/system/inspect/world-building(PCG)/gameplay(GAS/AI/combat)/audio/sequencer/networking,
  native C++ Automation Bridge) and the coding agent forgets these tools exist if
  it doesn't load them at session start. Master skill for any Unreal Engine project
  the owner is building (UE5, 5.0-5.8). Use whenever the session involves Unreal,
  UE5, .uproject, C++ gameplay code, Blueprints, Actors, Levels, World Partition,
  Niagara VFX, Sequencer/cinematics, UMG widgets, Enhanced Input, Gameplay Ability
  System (GAS), Behavior Trees / EQS / StateTree AI, Control Rig / animation BPs,
  MetaSound/audio, replication/networking, Nanite/Lumen, MetaHuman, Chaos physics,
  building/cooking/packaging via UBT, PIE (Play-In-Editor), or in-engine generative
  AI (prompt-to-3D via Meshy/Tripo/Rodin, LLM-driven NPCs, TTS).
---

Load the [Solaris workflow](resources/canonical/employees/engineering/unreal-developer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
