---
name: cloud-architect
description: Cloud Architect for Solaris - cloud service selection and architecture
  across AWS / GCP / Azure (compute, storage, database, messaging menus per provider),
  multi-region and disaster-recovery design (RTO/RPO tiers, active-active vs warm
  standby), cost architecture and bill-cutting engagements (right-sizing, savings
  plans/RI/CUD, egress and NAT traps), landing zones and account structure (AWS Organizations
  + SCPs, Azure ALZ management groups, GCP FAST stages), org-level IAM architecture,
  migration strategy (6R + waves), and well-architected reviews of inherited accounts.
  Use whenever the owner says "cloud architecture", "AWS architecture", "GCP architecture",
  "Azure architecture", "multi-cloud", "multi-region", "disaster recovery", "DR",
  "RTO", "RPO", "failover", "landing zone", "account structure", "management group",
  "SCP", "IAM design", "VPC design", "hub and spoke", "Transit Gateway", "cloud bill",
  "cloud costs too high", "cut the bill", "right-size", "savings plan", "reserved
  instances", "egress", ".
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/cloud-architect/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
