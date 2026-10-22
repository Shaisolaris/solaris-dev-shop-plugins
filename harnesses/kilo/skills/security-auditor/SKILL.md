---
name: security-auditor
description: Security Auditor for Solaris - penetration testing (manual + automated),
  threat modeling (STRIDE, PASTA, LINDDUN), vulnerability assessment, OWASP Top 10
  + ASVS + SAMM, mobile security (OWASP MASVS), cloud security posture (CSPM), container
  / Kubernetes security, secrets scanning, SAST / DAST / IAST / SCA, SBOM + supply
  chain security, compliance audits (SOC 2 Type I/II, ISO 27001, HIPAA, PCI-DSS, GDPR,
  CCPA), incident response + forensics, red team exercises, zero-trust architecture,
  identity + access review, security training + secure-code review. Use whenever the
  owner says "security audit", "pentest", "penetration test", "vulnerability", "OWASP",
  "threat model", "STRIDE", "SAST", "DAST", "SCA", "SBOM", "supply chain", "zero trust",
  "SOC 2", "ISO 27001", "HIPAA", "PCI", "GDPR", "CCPA", "security review", "secure
  code review", "secrets scan", "red team", "blue team", "incident forensics", "MASVS",
  "CSPM".
---

Load the [Solaris workflow](resources/canonical/employees/quality-security/security-auditor/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
