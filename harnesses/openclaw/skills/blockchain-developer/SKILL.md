---
name: blockchain-developer
description: 'Blockchain Developer for Solaris - Solidity/EVM smart contract engineering
  on real workflows (per wshobson blockchain-web3 plugin + nascentxyz simple-security-toolkit):
  secure dev pipeline (spec → risk evaluation → FREI-PI implementation → 8-rung test
  ladder → scripted deploy with state-transition tests), token standards (ERC-20/2612
  + vesting, ERC-721/1155 + EIP-2981 royalties, ERC-4626 vaults w/ inflation-attack
  defense, proxies UUPS/Transparent/Beacon/Diamond, ERC-4337 AA), audit-prep engagements
  (readiness checklist, scoping form, extraneous-assumptions doc), security patterns
  (CEI, pull-over-push, commit-reveal, circuit breakers, reentrancy/oracle/signature-replay/front-running
  defenses, weird-token matrix), testing (Foundry fuzz + invariant + mainnet-fork
  + gas snapshots, Hardhat fixtures + impersonation), launch ops (pre-launch checklist,
  monitoring/alerting, bug bounty sizing, incident response war room), DeFi primitives
  (staking rewards accounting, constant-product AMMs, lending, flash loans.'
---

Load the [Solaris workflow](resources/canonical/employees/engineering/blockchain-developer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
