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

Load the [canonical workflow](../../employees/data/data-scientist/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
