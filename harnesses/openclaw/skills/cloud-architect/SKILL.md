---
name: cloud-architect
description: Cloud Architect for Solaris - cloud service selection and architecture
  across AWS / GCP / Azure (compute, storage, database, messaging menus per provider),
  multi-region and disaster-recovery design (RTO/RPO tiers, active-active vs warm
  standby), cost architecture and bill-cutting engagements (right-sizing, savings
  plans/RI/CUD, egress and NAT traps), landing zones and account structure (AWS Organizations
  + SCPs, Azure ALZ management groups, GCP FAST stages), org-level IAM architecture,
  migration strategy (6R + waves), and well-architected reviews of inherited accounts.
  Use whenever the owner says cloud architecture, AWS architecture, GCP architecture,
  Azure architecture, multi-cloud, multi-region, disaster recovery, DR, RTO, RPO,
  failover, landing zone, account structure, management group, SCP, IAM design, VPC
  design, hub and spoke, Transit Gateway, cloud bill, cloud costs too high, cut the
  bill, right-size, savings plan, reserved instances, egress, .
---

Load the [canonical workflow](../../employees/infrastructure/cloud-architect/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
