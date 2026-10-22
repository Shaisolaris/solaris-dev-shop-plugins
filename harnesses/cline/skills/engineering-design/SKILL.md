---
name: engineering-design
description: 'Engineering Design (CAD) for Solaris - precise, parametric, manufacturable
  3D and electronics design. Use whenever the work needs real dimensions, tolerances,
  constraints, or printability: designing a 3D-printable part, a CNC/machined part,
  a parametric model that must update from a driving dimension, an assembly, a mechanical
  bracket/enclosure/jig, FEM stress sanity-checks, or exporting clean STEP/STL for
  manufacturing - and, when a part needs a circuit board, PCB design via KiCad. Triggers
  on "CAD", "FreeCAD", "parametric", "3D print this part", "printable", "STEP file",
  "STL", "tolerance", "enclosure", "bracket", "mechanical part", "assembly", "FEM",
  "stress check", "PCB", "KiCad", "circuit board". CONNECT employee - the host runs
  FreeCAD with the MCP addon (and the KiCad MCP server); this employee is the design
  doctrine. Distinct from artistic/organic 3D (Blender) and from ar-vr-developer (XR)
  and game-designer (game assets).'
---

Load the [Solaris workflow](resources/canonical/employees/specialized/engineering-design/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
