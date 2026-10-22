---
name: code-reviewer
description: '⚠️ ALWAYS load `code-context-operator.md` FIRST when reviewing or auditing
  a codebase larger than ~2,000 files (CTT, Turnpike, Kellbell, any inherited project
  takeover). Without semantic indexing, audits fall back to grep - which misses everything
  that doesn''t match exact strings. Code Reviewer for Solaris. Exhaustive code review,
  security audit, PR review, debug mode, dependency audit, CVE scanning, architecture
  review, first-principles review (Karpathy-style), adversarial review. v0.3.0 adds:
  zilliztech/code-context (semantic code search MCP via Milvus + Voyage/OpenAI/Gemini/Ollama
  embeddings + Merkle-tree incremental indexing - turns the entire codebase into context).
  Languages: JavaScript/TypeScript, Python, PHP, Ruby, Go, Rust, Java, C#, Swift,
  Kotlin, SQL. Frameworks: React, Next.js, Vue, Node.js, Express, FastAPI, Django,
  Laravel, Rails, Spring, .NET. Use whenever the owner says "code review", "review
  this PR", "review this diff", "audit the code", "find bugs", "check the code", "is
  this safe".'
---

Load the [Solaris workflow](resources/canonical/employees/quality-security/code-reviewer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
