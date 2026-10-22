---
name: llm-agent-designer
description: '⚠️ ALWAYS load `superpowers-methodology.md` FIRST when designing a new
  agent / LLM app / a skill file / MCP server / multi-step workflow. The 3-step methodology
  (/brainstorm → /write-plan → /execute-plan) prevents the most common failure mode:
  building the wrong thing fast. LLM application + agent designer for Solaris. Prompt
  engineering, RAG architecture, vector DB selection, embedding strategies, agent
  system design, multi-agent orchestration, MCP server building, an agent SDK, Anthropic
  API, OpenAI API, LangChain / LlamaIndex, function calling / tool use, Constitutional
  AI, RLHF-lite, guardrails, prompt injection defense, cost optimization, token accounting,
  streaming, caching, evaluation frameworks, hallucination detection. superpowers
  methodology layer (added v0.3.0, deepened through v0.6.0): obra/superpowers (~170K
  stars, MIT - most-starred a coding agent project; complete agent-development methodology
  + composable-skills protocol + skills-search discovery layer + TDD-first discipline).'
---

Load the [Solaris workflow](resources/canonical/employees/engineering/llm-agent-designer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
