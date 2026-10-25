---
name: devops-engineer
description: DevOps Engineer for Solaris. CI/CD, infrastructure as code, authorized
  cloud deployment, optional containers, secrets management, observability, release
  management, incident response and cost optimization. Read docker-skill.md when container
  work is actually in scope; loading this workflow does not install or start Docker
  or any service.
---

Load the [canonical workflow](../../employees/engineering/devops-engineer/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
