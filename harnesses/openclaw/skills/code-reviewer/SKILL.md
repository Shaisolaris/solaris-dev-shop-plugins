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

Load the [canonical workflow](../../employees/quality-security/code-reviewer/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
