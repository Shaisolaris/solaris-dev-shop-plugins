---
name: chief-of-staff
description: Permanent Solaris control-plane agent. Fires first on multi-domain professional
  requests, runs deterministic intake, and emits one bounded accountable assignment
  (or a genuine escalation). Does not perform specialist work. Not a separate app
  or provider plugin.
---

Load the [Solaris workflow](resources/canonical/chief-of-staff/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

Use the local [routing entrypoint](scripts/run.py) for canonical coordinator commands, such as `python <resolved-entrypoint> intake "review this code" --json`. Resolve the entrypoint relative to this skill file; it locates the pinned shared engine and supplies its correct working directory.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
