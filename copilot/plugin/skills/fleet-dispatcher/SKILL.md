---
name: fleet-dispatcher
description: Dispatches work to headless worker machines and checks on them using
  project-local fleet state. Fires on "send this to a worker", "dispatch to fleet/worker",
  "check the worker", "fleet status", "sync fleet", "is the stream done", or "bounce
  it back". Provider-neutral. Never reads personal Desktop paths; never silent-deploys
  or rewrites git history.
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/fleet-dispatcher/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
