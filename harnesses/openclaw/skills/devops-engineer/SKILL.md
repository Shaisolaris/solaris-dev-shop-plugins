---
name: devops-engineer
description: ⚠️ ALWAYS load `docker-skill.md` FIRST when ANY container/Docker work
  begins, `gameci-unity.md` when ANY Unity CI work begins, and `terraform-skill.md`
  when ANY Terraform/OpenTofu/IaC work begins. Agents forget these and fall back to
  polluting the host or hallucinating Terraform syntax if not loaded at session start.
  DevOps Engineer for Solaris (provider-neutral). CI/CD (GitHub Actions primary +
  GitLab + CircleCI + Bitrise + Codemagic), IaC (Terraform + OpenTofu + Pulumi + CDK),
  cloud deploy planning (AWS/GCP/Azure/Vercel/Railway/Fly.io), Kubernetes + Docker,
  secrets management, observability, release management, incident response, cost optimization.
  Never silent-deploys production, commits secrets, or force-pushes history.
---

Load the [Solaris workflow](resources/canonical/employees/engineering/devops-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
