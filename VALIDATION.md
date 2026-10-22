# Native package validation for 0.64.0

Core source: [`3a577e42`](https://github.com/Shaisolaris/solaris-dev-shop/commit/3a577e42c48473f6ef8680950dd55c067820d5d3). Tested native payloads: [`2e51c951`](https://github.com/Shaisolaris/solaris-dev-shop-plugins/commit/2e51c951ce4573c0ab7c5cc807118d6e0c5b815c). Complete file hashes and executable modes bind the source; later product changes require affected checks to run again. The roster remains 61 specialists plus a coordinator, and all 1,197 canonical files retain their source bytes.

## Correctness and security repairs

- Existing destinations are refused by the QA skill-copy operation, including broken symlinks and source-checkout destinations. A race cannot trigger deletion of an existing directory. Five regression tests failed against the old source and passed against the repair; useful copy and cleanup paths also passed.
- Network instructions retain TLS certificate verification with an explicit trusted CA and expected server name. Actual Caddy controls accepted trusted identity, rejected wrong CA/name, demonstrated the unsafe negative control and recovered successfully. Linux CI executes this gate.
- WordPress instruction blocks use data transport rather than interpolating directory/flag values into Python or a second SSH shell. Real local fixtures reproduced old code execution and demonstrated corrected useful JSON/Git results and recovery. Fake SSH is confined to the fixture; no real site is contacted.
- Independent review reproduced the fixes and withdrew a separate incorrect Bash quote-expansion finding after five literal-input controls. A lexical scanner row is not automatically either a vulnerability or a clean result.

## Exact source and useful outcomes

Core [PR50 CI](https://github.com/Shaisolaris/solaris-dev-shop/pull/50/checks) passed all eight jobs, including supported Linux/macOS/Windows lanes, quality/manifests and actual TLS checks. The final source also passed the G39 delivery/interruption/recovery oracle 18/18, G40 portability oracle 8/8, G41 inventory/release-gate oracle 10/10 and G42 cross-checks with zero findings. A clean 0.64 wheel installed outside the checkout passes self-test, useful code-review intake and skill lookup; all eight packaged runtime members match the declared canonical source. The wheel supplies the routing package; complete specialist resources are supplied by native distributions.

The independent pinned base builder remains `129781961be54cc2f12d6bafe80e81d6a1cd8d02`. Its rebuild matches the base package and both catalogs, rejects nine artifact controls and two listing-metadata regressions, and executes the actual coordinator. The default contained builder applies notices and CI relocation once. Frozen input `b13ca3c` is explicitly unfinished, and a negative control proves it fails final verification.

Native [PR12 CI](https://github.com/Shaisolaris/solaris-dev-shop-plugins/pull/12/checks) checks every profile byte/mode and real callers, generic provenance and cross-checks, plus fresh native Linux Antigravity/OpenClaw, Cline local/public Git and Amp registered callback execution. The source profile counts and actual host scopes are in [HARNESS-DISTRIBUTION.md](HARNESS-DISTRIBUTION.md). Complete standalone native PRs also run independent fresh Linux checks: [Kilo2](https://github.com/Shaisolaris/solaris-dev-shop-kilo/pull/2), [OpenClaw3](https://github.com/Shaisolaris/solaris-dev-shop-openclaw/pull/3), [Antigravity2](https://github.com/Shaisolaris/solaris-dev-shop-antigravity/pull/2), [Gemini3](https://github.com/Shaisolaris/solaris-dev-shop-gemini/pull/3).

Independent distribution review executed the golden/refusal controls, checked repaired-source propagation, all standalone profile equivalences, exactly-once notices and identical decoded icon pixels. The icon provenance record now distinguishes the unchanged base icon from its lossless OpenClaw encoding variant. Local native runtime evidence and source review have different scopes; neither is marketplace approval.

## Explicit limits

No model inference, company/private-repository grant, new background scheduler or scanner bypass was required by these checks. Native inventory does not prove model quality or a filesystem sandbox. Test skips are explicit; the real offline-wheel and TLS cases were separately executed rather than converted to success by skipping them. Google's strict manifest produces one retained generic missing-license-field policy finding despite its real MIT license; all other provenance findings are rejected. Hermes admission is held by its native scanner. Registry login, provider eligibility and curator decisions remain separate publication gates.

Previous source/runtime records remain in [the 0.63 history](docs/history/VALIDATION-063.md); they are not relabeled as fresh 0.64 execution. The final release artifacts must retain exact source manifests, checksums, version/roster/branding agreement and clean CI. No old tag or release asset is rewritten.
