---
name: fleet-dispatcher
description: Dispatches work to headless worker machines and checks on them using
  project-local fleet state. Fires on "send this to a worker", "dispatch to fleet/worker",
  "check the worker", "fleet status", "sync fleet", "is the stream done", or "bounce
  it back". Provider-neutral. Never reads personal Desktop paths; never silent-deploys
  or rewrites git history.
---

Load the [canonical workflow](../../employees/infrastructure/fleet-dispatcher/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
