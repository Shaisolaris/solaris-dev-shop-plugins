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

Load the [canonical workflow](../../employees/data/data-engineer/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
