---
name: fleet-provisioner
description: Provisions a machine as a headless worker with project-local fleet registration.
  Fires on "make this machine headless", "provision this mini/laptop", "add this machine
  to the fleet", or "decommission this machine". Provider-neutral. Never stores tokens
  in git; never depends on personal Desktop paths; never silent-deploys production
  apps.
---

Load the canonical Solaris workflow at [fleet-provisioner](../../employees/infrastructure/fleet-provisioner/SKILL.md). Resolve that path relative to this SKILL.md, then use its instructions and companion files. Run helpers from their canonical role folder so shared imports and resources remain valid. The host supplies execution tools and permissions; this adapter adds no grants or background jobs.
