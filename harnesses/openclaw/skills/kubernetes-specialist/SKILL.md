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

Load the [canonical workflow](../../employees/infrastructure/kubernetes-specialist/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
