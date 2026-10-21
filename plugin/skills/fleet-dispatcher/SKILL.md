---
name: fleet-dispatcher
description: Dispatches work to headless worker machines and checks on them using
  project-local fleet state. Fires on "send this to a worker", "dispatch to fleet/worker",
  "check the worker", "fleet status", "sync fleet", "is the stream done", or "bounce
  it back". Provider-neutral. Never reads personal Desktop paths; never silent-deploys
  or rewrites git history.
---

Load the canonical Solaris workflow at [fleet-dispatcher](../../employees/infrastructure/fleet-dispatcher/SKILL.md). Resolve that path relative to this SKILL.md, then use its instructions and companion files. Run helpers from their canonical role folder so shared imports and resources remain valid. The host supplies execution tools and permissions; this adapter adds no grants or background jobs.
