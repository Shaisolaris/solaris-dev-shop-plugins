# Native package validation

The current 0.63.0 repair candidate pins Solaris Dev Shop core 0.63 at
[`ee38d3de3d4b0d5467a589d5cb908f4964f593fe`](https://github.com/Shaisolaris/solaris-dev-shop/commit/ee38d3de3d4b0d5467a589d5cb908f4964f593fe).
`BUILD.json` and `plugin/SOLARIS-BUILD-SOURCE.json` bind every shipped source file to that revision.
The published release tags and assets remain unchanged; this is a packaging repair candidate, not a new release.

## Current repair evidence

- The core change replaces a routing guide that named a removed script. Its four current examples resolve to the expected capabilities; all nine routing regression tests pass. Runtime implementation code is unchanged from the published 0.63 source. The G42 integration plan now permits this exact routing-guide path; its matching scope test was updated, while a neighboring file remains denied. Three plan tests pass locally; the final core CI gate binds the complete source revision.
- The native coordinator now links directly to its engine and distinguishes the plugin root from the canonical role folder. Following the former instructions failed with exit 2. The new verifier resolves the entrypoint from the native skill and obtains a real `solaris.code-reviewer` assignment from a different working directory; it checks that the coordinator performed no specialist work.
- An independently pinned rebuild matches all 1,196 canonical files and the generated payload/catalogs. Nine artifact tampering controls and the two actual listing regressions (overlong subtitle and missing software terms) are rejected.
- The subtitle is 23 characters and the software terms point to the existing MIT license. The data-handling document names its provenance record instead of carrying an obsolete source-version label.
- Fresh native-host installation checks for this repair are pending. The published-base host evidence below must not be represented as a fresh installation of this updated candidate.

## Published 0.63.0 base evidence

These checks used core revision `9f8cc53d3b84c78d3d26433948e2e0bdcc1b5bd5` and the original package. They establish the baseline and their stated scope, not the corrected caller instructions above.

- All 1,196 shipped canonical files match upstream bytes. The upstream README is preserved as `SOURCE-README.md`; repository `.gitignore` is deliberately omitted. The original 61 specialist roles, coordinator and artwork remain intact.
- A rebuild with the independently pinned packager matches the complete generated payload and both catalogs, including executable modes. All nine built-in tampering controls are rejected. A separate independent audit also rejected eleven additional controls against the same verifier implementation.
- The implementation and tests are unchanged from independently reviewed [`5b4e9c9`](https://github.com/Shaisolaris/solaris-dev-shop/commit/5b4e9c9ec4994554dba1459fb4e5c82f2017bf1e). That source passed [all seven CI jobs](https://github.com/Shaisolaris/solaris-dev-shop/actions/runs/39696362889), including 907-test Linux/macOS lanes with explicit skips and the documented supported Windows lane. The final 0.63 metadata revision has its own CI gate.
- Codex freshly installed 0.63.0 under an isolated test catalog. All 1,268 installed payload files matched the candidate; the installed router self-test and 18-case delivery/recovery oracle passed outside the source checkout. The temporary test catalog was removed afterward. The 0.62 app-server discovery result remains historical evidence, not a claimed fresh 0.63 model invocation.
- Claude Code 2.1.306 freshly installed 0.63.0 in an owned isolated configuration, reported 62 skills in its native inventory, and retained all 1,268 candidate payload files byte-for-byte.
- OpenCode 2.1.2 loaded 0.63.0 from exact public Git commit `73631073ce689e1e6d98a2af6bc95cecb5fe8fc2`. Its authenticated local HTTP catalog reached 62 Solaris workflows, all contents matched the canonical files, and its cache matched all 1,196 source hashes. The bounded test server was terminated and waited for after validation.
- GitHub Copilot CLI 1.0.102 added the public `solaris-technologies` marketplace and installed `solaris-dev-shop@solaris-technologies` in an isolated configuration. Its native inventory contained all 62 workflows with matching names, descriptions, paths and enabled states. All 1,268 payload files matched the published ZIP; the installed router self-test and 18-case delivery oracle passed outside the source checkout. A separate instruction-following check then found the coordinator working-directory defect addressed above. No model activation or GitHub-curated approval is claimed.
- The native loading implementation and discovery adapter bytes are unchanged from 0.62. Test-catalog names isolate the Codex/Claude installations; they do not alter the plugin payload or grant provider approval.

## Verification scope

Source, native discovery and local helper checks do not prove model-driven activation quality, provider-directory approval or every role's performance on real customer work. Some helpers require POSIX or additional documented tools. No model invocation or new account permission is granted by installing this package. Raw account state and host catalogs remain private.

## Run the conformance checks

```sh
python -m pip install PyYAML==6.0.3
python tools/verify_distribution.py --source /path/to/pinned-upstream-checkout \
  --packager /path/to/reviewed-packager-checkout --self-test
```

The packager checkout must be exactly `129781961be54cc2f12d6bafe80e81d6a1cd8d02` from the Solaris source repository. Its builder and assets must match that Git revision. The verifier independently rebuilds every generated byte; an adjacent payload manifest cannot authorize changed code. Nine negative controls cover canonical source, revision, workflow index, adapter instructions, native loaders, lifecycle scripts and extra catalog entries. Separate checks reject the two listing regressions and exercise the coordinator entrypoint resolved from the native skill.
