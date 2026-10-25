---
name: chief-of-staff
description: Permanent Solaris control-plane agent. Fires first on multi-domain professional
  requests, runs deterministic intake, and emits one bounded accountable assignment
  (or a genuine escalation). Does not perform specialist work. Not a separate app
  or provider plugin.
---

Load the [canonical workflow](../../chief-of-staff/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

Use the [guarded routing entrypoint](scripts/run.py), for example `python <resolved-entrypoint> intake "review this code" --json`. It selects the canonical working directory and returns an assignment without performing specialist work.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
