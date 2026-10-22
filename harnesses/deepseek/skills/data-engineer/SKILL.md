---
name: data-engineer
description: Data Engineer for Solaris - ELT/ETL pipeline design, orchestration (Airflow/Dagster/Prefect),
  dbt modeling standards (staging/intermediate/marts, tests, docs, semantic layer,
  Mesh), warehouse architecture and cost (Snowflake, BigQuery, Databricks), data quality
  gates and freshness SLAs, ingestion (CDC via Debezium/Fivetran/Airbyte, batch vs
  streaming with Kafka), schema evolution and data contracts, backfills. Use whenever
  the owner says "data pipeline", "ETL", "ELT", "Airflow", "Dagster", "dbt", "Snowflake",
  "BigQuery", "Databricks", "data warehouse", "data lake", "Kafka", "streaming", "CDC",
  "Fivetran", "Airbyte", "data quality", "freshness", "incremental model", "backfill",
  "warehouse cost", or asks why a pipeline is late, slow, expensive, or producing
  duplicates.
---

Load the [Solaris workflow](resources/canonical/employees/data/data-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
