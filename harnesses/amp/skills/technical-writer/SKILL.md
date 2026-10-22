---
name: technical-writer
description: Technical Writer for Solaris - documentation standards + client-facing
  technical docs. Diátaxis-driven doc-type selection (tutorial / how-to / reference
  / explanation via the compass), API documentation (OpenAPI 3.1 specs, per-endpoint
  8-point contract, multi-language samples, Swagger UI / Redoc / Mintlify / ReadMe
  portals), README authoring under a zero-hallucination scan protocol, user guides
  for client products (task-based, audience-split), runbook standards (six mandatory
  step attributes) + handoff documentation packs, long-form technical manuals (docs-architect
  3-phase, 10 sections), CHANGELOG (Keep a Changelog 1.1.0) + release notes + Conventional
  Commits + SemVer, ADRs (MADR), Mermaid + C4 diagrams-as-code, readability + AI-ism
  scrubbing, docs maintenance discipline (Minimum Viable Documentation, delete dead
  docs), docs-for-AI-agents deliverable (llms.txt + llms-full.txt - the B2A docs standard
  coding agents fetch). Use when the owner says "documentation", "docs", "API docs",
  "OpenAPI", "Swagger".
---

Load the [Solaris workflow](resources/canonical/employees/design/technical-writer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
