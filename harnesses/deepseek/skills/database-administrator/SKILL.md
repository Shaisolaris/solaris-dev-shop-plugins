---
name: database-administrator
description: 'Database Administrator for Solaris - schema design, query optimization,
  migration execution, backup + restore, replication, failover, indexing strategy,
  partitioning, sharding, capacity planning. Databases: PostgreSQL (primary for most
  Solaris work), MySQL / MariaDB, SQLite, MongoDB, DynamoDB, Redis + Redis Cluster,
  Elasticsearch, Cassandra, Snowflake / BigQuery (analytical). Use whenever the owner
  says "database", "DB", "schema", "slow query", "query optimization", "explain plan",
  "index", "indexing", "migration", "backup", "restore", "replication", "read replica",
  "failover", "PostgreSQL", "Postgres", "MySQL", "MongoDB", "Redis", "sharding", "partitioning",
  "data model", "normalization", "denormalization", "ORM performance", "N+1".'
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/database-administrator/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
