---
name: project-onboarding
description: Runs a local project activation sequence. Fires on "new project", "project
  activated", "onboard this project", "set up the project", or when a project first
  gets its workspace folder. One short plain-chat intake, then a conservative local
  setup with activate.py - folders, STATUS.md with the recorded deploy model, credential
  locations, round plan, and a read-only Git check - that preserves existing owner
  files and resumes after interruption. Never deploys, stores secrets or changes CI.
---

Load the [Solaris workflow](resources/canonical/employees/product-project/project-onboarding/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
