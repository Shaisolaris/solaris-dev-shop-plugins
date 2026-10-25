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

Load the [canonical workflow](../../employees/specialized/payments-specialist/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
