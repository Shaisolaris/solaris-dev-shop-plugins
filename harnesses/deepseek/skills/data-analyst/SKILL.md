---
name: data-analyst
description: Data Analyst for Solaris - SQL analysis (CTEs, window functions, EXPLAIN
  review, query optimization for analytics), dashboards + KPI design (Metabase, Looker,
  Tableau, Power BI, Superset, Grafana, Streamlit), metric definitions and SaaS metrics
  (MRR, ARR, churn, CAC, LTV, NRR, Quick Ratio), cohort + funnel + retention analysis,
  A/B test result interpretation, data-quality gating before analysis, instrumentation/tracking
  audits, data storytelling and executive reporting. Use whenever the owner says "dashboard",
  "report", "SQL query", "analyze data", "metrics", "KPI", "metric definition", "cohort",
  "funnel", "retention", "LTV", "churn", "MRR", "A/B results", "did the test win",
  "why did X drop", "business question", "chart", "visualization", "Looker", "Tableau",
  "Metabase", "Power BI", "tracking plan", "can we trust this data", "what does the
  data say", "how are we doing on X".
---

Load the [Solaris workflow](resources/canonical/employees/data/data-analyst/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
