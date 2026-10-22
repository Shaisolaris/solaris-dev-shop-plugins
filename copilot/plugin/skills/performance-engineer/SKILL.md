---
name: performance-engineer
description: Performance Engineer for Solaris - profiling (Node.js, Python, Go, Rust,
  Java, PHP, web frontend, mobile), bundle analysis, load / stress / soak testing,
  PageSpeed + Lighthouse + Web Vitals optimization, capacity planning, APM interpretation
  (Datadog, New Relic, AppDynamics, Dynatrace), database query optimization, caching
  strategy (Redis, CDN, browser), memory profiling (heap dumps, leak detection), CPU
  profiling (flame graphs), mobile perf (frame time, jank, battery), cold-start optimization
  (serverless), network optimization (HTTP/2, HTTP/3, QUIC, compression). Use whenever
  the owner says "performance", "slow", "latency", "throughput", "bundle size", "PageSpeed",
  "Lighthouse", "Web Vitals", "LCP", "CLS", "INP", "FID", "TTFB", "load test", "stress
  test", "profile", "flame graph", "heap dump", "memory leak", "CPU usage", "cold
  start", "bundle analysis", "optimize", "cache", "CDN".
---

Load the [Solaris workflow](resources/canonical/employees/quality-security/performance-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
