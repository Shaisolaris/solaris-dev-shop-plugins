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

Load the [canonical workflow](../../employees/engineering/llm-agent-designer/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
