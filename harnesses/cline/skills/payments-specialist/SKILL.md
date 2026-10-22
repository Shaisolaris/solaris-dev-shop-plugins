---
name: payments-specialist
description: ⚠️ ALWAYS load stripe-mcp-operator.md FIRST when Stripe + AI agents +
  token billing are involved. Payments Specialist for Solaris - Stripe integration
  (Checkout Sessions, Payment Intents, Setup Intents, webhook architecture, subscription
  components per wshobson) + Stripe agent-toolkit / MCP server / token-meter (official
  stripe/ai monorepo - agent-mediated payment ops + AI-product usage billing), payment
  flows (one-time, subscription, marketplace, escrow, agentic commerce), PCI compliance
  + tokenization (Stripe.js, Stripe Elements, hosted Checkout), webhook reliability
  (idempotency keys, retry handling, signature verification), Strong Customer Authentication
  (SCA) for European payments (3D Secure, PSD2), payment method management (cards,
  wallets, ACH, SEPA, iDEAL, Klarna, Afterpay), refunds + disputes + chargebacks (evidence
  collection, response automation), subscription billing (proration, plan changes,
  pausing, dunning, smart retries), invoice generation, tax calculation (Stripe Tax,
  TaxJar, Avalar.
---

Load the [Solaris workflow](resources/canonical/employees/specialized/payments-specialist/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
