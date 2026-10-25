---
name: project-onboarding
description: Runs a local project activation sequence. Fires on "new project", "project
  activated", "onboard this project", "set up the project", or when a project first
  gets its workspace folder. One short plain-chat intake, then a conservative local
  setup with activate.py - folders, STATUS.md with the recorded deploy model, credential
  locations, round plan, and a read-only Git check - that preserves existing owner
  files and resumes after interruption. Never deploys, stores secrets or changes CI.
---

Load the [canonical workflow](../../employees/product-project/project-onboarding/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
