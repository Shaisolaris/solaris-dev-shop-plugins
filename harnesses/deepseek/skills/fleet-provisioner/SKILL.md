---
name: fleet-provisioner
description: Provisions a machine as a headless worker with project-local fleet registration.
  Fires on "make this machine headless", "provision this mini/laptop", "add this machine
  to the fleet", or "decommission this machine". Provider-neutral. Never stores tokens
  in git; never depends on personal Desktop paths; never silent-deploys production
  apps.
---

Load the [canonical workflow](../../employees/infrastructure/fleet-provisioner/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
