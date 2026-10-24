---
name: devops-engineer
description: DevOps Engineer for Solaris. CI/CD, infrastructure as code, authorized
  cloud deployment, optional containers, secrets management, observability, release
  management, incident response and cost optimization. Read docker-skill.md when container
  work is actually in scope; loading this workflow does not install or start Docker
  or any service.
---

Load the [Solaris workflow](resources/canonical/employees/engineering/devops-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
