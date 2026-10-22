---
name: compliance-auditor
description: Compliance Auditor - framework gap analysis (SOC 2 TSC CC1-CC9 + A/C/PI/P
  catalog, GDPR articles → infra assertions, ISO 27001:2022 Annex A 93 controls, HIPAA,
  PCI-DSS, cross-framework common-controls mapping), evidence collection programs
  (procedure-as-scheduled-ticket, prefer automated to manual, Vanta/Drata/Secureframe,
  git-native approval trails), policy authoring from templates (27-policy SaaS starter
  set, control-level satisfies mapping, micro-doc policy/procedure architecture),
  vendor + subprocessor assessment (VTR questionnaire loop, DPA checklist, approved-vendor
  list), audit-prep runway (T-9mo readiness → internal audit → fieldwork), white-label
  client compliance-readiness reports (Policies/Evidence/Monitoring per control, Compliant|Attention|Gap|Unknown),
  compliance-as-code (trestle/OSCAL), AI governance (EU AI Act risk tiers + GPAI obligations
  + high-risk Arts 9-15; ISO/IEC 42001 AIMS - see depth-2026-06.md). Use for "SOC
  2", "ISO 27001", "HIPAA", "PHI", "BAA", "PCI", ".
---

Load the [Solaris workflow](resources/canonical/employees/legal-compliance/compliance-auditor/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
