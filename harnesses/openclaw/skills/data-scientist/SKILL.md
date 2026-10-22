---
name: data-scientist
description: Data Scientist for Solaris - experiment design (gated A/B setup, power
  analysis, sample size, randomization, stratification), statistical inference discipline
  (test selection, Welch's t, Wilson CIs, peeking/multiple-comparison control, Bayesian-vs-frequentist
  calls), causal inference (diff-in-diff, propensity score, regression discontinuity,
  synthetic control - with honest assumption checks), forecasting (three-number forecasts
  with assumption blocks, CoV confidence bands, cohort decomposition), and the statistical
  QA gate Data Analyst escalates to. Use whenever the owner says "design an A/B test",
  "sample size", "power analysis", "is this significant", "p-value", "confidence interval",
  "causal", "did the change cause", "diff-in-diff", "propensity", "regression discontinuity",
  "forecast", "Bayesian", "bandit", "sequential test", "the analyst's numbers look
  off", "experiment methodology".
---

Load the [Solaris workflow](resources/canonical/employees/data/data-scientist/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
