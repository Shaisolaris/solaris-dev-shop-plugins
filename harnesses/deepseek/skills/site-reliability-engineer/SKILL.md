---
name: site-reliability-engineer
description: Site Reliability Engineer for Solaris - SLOs / SLIs / error budgets,
  burn-rate alerting, alert design, on-call rotations and handoffs, incident command
  (SEV1-SEV5), blameless postmortems, runbook engineering, observability design (golden
  signals, RED/USE, logs, traces), production readiness reviews. Use whenever the
  owner says "SLO", "SLI", "SLA", "error budget", "uptime", "availability", "downtime",
  "site is down", "client site down", "outage", "incident", "on-call", "pager", "PagerDuty",
  "Opsgenie", "postmortem", "post-mortem", "blameless", "runbook", "observability",
  "alerting", "alert fatigue", "burn rate", "status page", "war room", "severity",
  "SEV1", "production readiness", "game day", "MTTR".
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/site-reliability-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
