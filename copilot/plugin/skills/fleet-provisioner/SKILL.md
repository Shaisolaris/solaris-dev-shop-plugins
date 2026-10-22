---
name: fleet-provisioner
description: Provisions a machine as a headless worker with project-local fleet registration.
  Fires on "make this machine headless", "provision this mini/laptop", "add this machine
  to the fleet", or "decommission this machine". Provider-neutral. Never stores tokens
  in git; never depends on personal Desktop paths; never silent-deploys production
  apps.
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/fleet-provisioner/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
