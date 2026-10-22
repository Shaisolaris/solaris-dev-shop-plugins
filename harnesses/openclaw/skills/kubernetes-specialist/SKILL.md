---
name: kubernetes-specialist
description: Kubernetes Specialist for Solaris - workload design (probes, resources,
  QoS, PDB, HPA/VPA/KEDA, topology spread, graceful shutdown), cluster architecture
  (EKS/GKE/AKS, CNI, ingress + Gateway API, storage, node pools), Kubernetes security
  (RBAC, NetworkPolicy, Pod Security Admission, admission policies with CEL/Kyverno/Gatekeeper,
  workload identity, External Secrets), multi-tenancy (namespace-per-team, quotas,
  team RBAC), upgrades + capacity + cost right-sizing, DR (Velero), and troubleshooting
  trees (CrashLoopBackOff, OOMKilled, Pending pods, ImagePullBackOff, DNS failures).
  Use whenever the owner says "Kubernetes", "k8s", "cluster", "pod", "manifest", "Deployment",
  "StatefulSet", "probe", "liveness", "readiness", "OOMKilled", "CrashLoopBackOff",
  "ImagePullBackOff", "pending pods", "evicted", "HPA", "VPA", "KEDA", "autoscaling",
  "PDB", "resource limits", "QoS", "RBAC", "NetworkPolicy", "Pod Security", "PSA",
  "Kyverno", "Gatekeeper", "admission policy", "service account", "ingress", "Gateway
  API", "CNI", ".
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/kubernetes-specialist/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
