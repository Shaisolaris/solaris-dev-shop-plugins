# Solaris native harness distributions

**61 specialist employees + one chief-of-staff coordinator = 62 workflows.**
These distribution adapters preserve the reviewed 0.63.0 source and add zero new employee capabilities. Existing core/native release tags and assets are unchanged.

## OpenCode V2

```sh
opencode plugin add 'github:Shaisolaris/solaris-dev-shop-plugins#53009f7ade20264183e8fa4ef3bc739a72299389::path:plugin'
```

OpenCode 2.1.2 installed this exact public revision. Its actual HTTP skill catalog exposed all 62 canonical workflows; all 1,268 installed file bytes and executable modes matched. The installed coordinator assigned a code review from outside the checkout. The official ecosystem submission is [PR58104](https://github.com/anomalyco/opencode/pull/58104), awaiting maintainer review.

## DeepSeek Harness

The native package at `harnesses/deepseek` declares a Cordis bundle and requires DSH **0.2.1-rc.2**, whose APIs are pre-stable. Install the complete package with `dsh plugin --profile <your-profile> add <package-source>`. For local authoring:

```sh
dsh plugin --profile solaris-test add ./harnesses/deepseek
dsh --profile solaris-test --dump-config
```

Install the reviewed public Git revision:

```sh
dsh plugin --profile solaris-test add "git+https://github.com/Shaisolaris/solaris-dev-shop-plugins.git#c69fbcf49e46da3837fcf75420b9914705b2eab7&path:/harnesses/deepseek"
```

A format1 custom-market index is published at `markets/deepseek.json`; it pins the same exact source. DSH ships no default public index and custom-market publication is not DeepSeek approval. The first-party index validator accepts this index and computes the same pinned install target.

The actual DSH plugin manager installed the bundle and the actual composed profile registered all 62 workflows. Every native loaded body and resource directory matched the canonical source. Registration is a framework-managed effect; the adapter declares no tool, hook, model, credential source or background schedule.

## Kilo

`harnesses/kilo` is a self-contained server plugin. Its manifest exposes `./server` and its V2 adapter contributes exactly the 62 reviewed skill rows, preventing recursive resource mirrors from becoming extra skills. It has no npm runtime dependencies.

Kilo **7.8.15** installed the local package through its real plugin manager. Its actual `/api/skill` V2 registry returned precisely 62 matching names, bodies and canonical locations. The legacy `debug skill` command is a separate catalog and is not the acceptance evidence for this V2 package. No permission, provider or model settings are modified.

For local authoring:

```sh
kilo plugin file:///absolute/path/to/harnesses/kilo
```

The public root package now has a verified native install route. Keep the package name before `@github:`:

```sh
kilo plugin 'solaris-dev-shop-kilo@github:Shaisolaris/solaris-dev-shop-kilo#3e3c611e82bee0885721c238e5c09fd5dc0d7d13'
```

This exact source passed the actual Kilo7.8.15 V2 API on macOS: all62 canonical bodies/descriptions/locations,1972 profile files and modes,1196 original hashes,62 real helper contexts and a coordinator assignment. The same full verifier passed on a fresh Linux CI runner. See [the public package and bounded proof](https://github.com/Shaisolaris/solaris-dev-shop-kilo/pull/1).

The unnamed npm Git references and catalog-style `git:` transport still report installer success but expose zero Solaris rows. The official catalog does not accept the passing named npm-compatible Git syntax; catalog submission remains held while [the existing V2 Git-source migration issue](https://github.com/Kilo-Org/kilocode/issues/15307#issuecomment-6345057436) is resolved. No schema bypass or unpublished npm-registry claim is used. These are native discovery/helper results, not model inference, VS Code or TUI-session acceptance.

## Qwen Code

Qwen Code **0.26.0** directly installed the existing public Gemini-format source below, converted its manifest through the native manager, and lists 62 enabled skill entries:

```sh
qwen extensions install https://github.com/Shaisolaris/solaris-dev-shop-gemini --ref ef92e4bd85a7b9971591812e2976210fd71fa851
```

All1977 installed source files and executable modes match the public revision; all62 context calls and the installed coordinator pass outside the checkout. This uses the host's documented cross-format support, with the complete source and resources retained. It is not an independent Qwen directory approval.

## Pi

The repository-root `package.json` is a native Pi package manifest. It declares the 62 exact skill files from the existing contained profile; it declares no extensions, prompts or themes. Pi **1.4.0** installed the local package, then its public native package resolver and skill loader found all 62 unique names with no diagnostics. The actual public Git install at `c69fbcf49e46da3837fcf75420b9914705b2eab7` also passes all62 names through the native manager and loader. All1974 contained payload file bytes/modes match; all62 live context calls and the installed coordinator work outside the checkout. The Pi gallery indexes npm packages; npm publisher authentication is a separate unresolved requirement.

## Kimi Code

The root `kimi.plugin.json` declares62 exact contained skill directories and no hooks, MCP servers, agents, credentials or session-start instructions. Kimi Code2.3.0's actual authenticated loopback native plugin API installed `c69fbcf49e46da3837fcf75420b9914705b2eab7` from public GitHub and reports enabled/stateOK/skillCount62 with no diagnostics. All1974 contained payload bytes/modes and62 live context calls/coordinator routing match. Install this complete repository through Kimi's `/plugins install` using the exact GitHub revision. Vendor catalog consideration is [issue4344](https://github.com/MoonshotAI/kimi-code/issues/4344); no curated or partner status is claimed.

## OpenClaw

The `harnesses/openclaw` profile is a native source plugin for OpenClaw2026.10.5. It declares all62 skills and a real `openclaw solaris intake <request> --json` command. That command invokes the pinned Python coordinator with argument separation, no shell, a32KiB input limit,20second timeout and a minimal child environment. It returns an assignment and never executes specialist work. Python3.10+ is required on the caller'sPATH. There are no model calls, MCP servers, background jobs or provider credentials.

The actual host loads the native plugin and registers the CLI. Its command returns a code-review assignment as JSON onstdout; literal shell syntax and option-like request text remain data, and oversized text is rejected. The first-party package inspector reports no issues. A golden rebuild checks all1974 source files/modes and1196 canonical hashes. Public transport and registry acceptance are separate gates.

An earlier compatible Agent Plugins bundle is publicly installable from `Shaisolaris/solaris-dev-shop-openclaw` at its exact reviewed marketplace revision; it exposes62 visible workflows. The native SDK and notice-repair revisions passed independent review and exact-source CI. The public default now carries the native SDK profile. Registry publication uses a complete compressed source artifact, preserving Unicode fixtures and every canonical file; no compiled or opaque executable is introduced.

## Google Antigravity

A distinct strict native profile is public at [solaris-dev-shop-antigravity](https://github.com/Shaisolaris/solaris-dev-shop-antigravity). Actual Antigravity CLI1.4.5 in a fresh hosted Linux profile installed/enabled the plugin, discovered62 workflows and passed complete payload bytes/modes,62 helper contexts and the coordinator outcome. The1971-file profile is checked against the reviewed source; the publication repository adds its own docs/CI. Google's official marketplace interest form confirmed receipt. See [the exact validation scope](ANTIGRAVITY-DISTRIBUTION.md). No existing Google profile or retired worker was changed, and no model call was made. Submission is not Google approval.

## Cline

`harnesses/cline` is a native Cline package plugin: its `cline.plugins` manifest names the real SDK entrypoint, its top-level skills are discovered by Cline, and its `solaris_intake` tool runs the pinned local coordinator. ClineCLI3.0.73 and SDK0.0.95's actual worker and ContributionRegistry registered and executed that tool. All62 owned skill descriptions/bodies/paths match; the input controls keep shell text and option-like text literal and reject oversized UTF-8 or extra fields. A valid request remains usable after refused calls. No model inference is involved.

The source profile has1973 files/modes and1196 canonical files. The native installer removes exactly two optional host-provided SDK dependency fields from `package.json`; the verifier checks that transformation explicitly and rejects any other change. All1972 other source files and all executable modes remain exact. The real composite provenance checker reports consistency. Source golden checks exercise62 real helper contexts plus6 no-op/partial/mode/hook/symlink refusals.

The exact public source root is installable through the native manager:

```sh
cline plugin install 'https://github.com/Shaisolaris/solaris-dev-shop-cline.git@7730f2a9a9246479b66da059598f4e54ef80f6c1'
```

A fresh public Git install passed the same native discovery, worker tool, source and helper gates. The manager retains its own clone metadata: the verifier binds HEAD and origin to the requested public commit and permits sample hooks only, while accounting separately for all1973 product files. It does not delete metadata or weaken npm policy. The official collection's formatting rules conflict with byte-preserved canonical documentation, so its prepared entry uses the normal versioned source-package dependency format. The npm package is ready but unpublished pending publisher authentication; no catalog keyword or approval is claimed.

This route targets ClineCLI/SDK/Kanban. Cline's current plugin documentation explicitly excludes VSCode and JetBrains extensions. Its official curated collection submission follows actual public Git installation and independent review; candidate source alone is not catalog approval. Python3.10+ and PyYAML are required for the local tool. It has no hooks, background jobs, MCP servers, model settings or permission changes.

## Amp

`harnesses/amp` is a complete native directory plugin using Amp's `registerSkill` and `registerTool` APIs. Install the complete directory at `.amp/plugins/solaris-dev-shop` in the target project, rather than importing its entrypoint alone. Python3.10+ and PyYAML are required for local helpers.

The actual authenticated AmpCLI0.0.1792680614-g8973a3 loaded the plugin and its `solaris_intake` tool. Its stock `skills list --json` exposed precisely62 qualified Solaris workflows; every name, description and registered path matched the unchanged bundled skill source. The profile retains1973 files/modes,1196 canonical hashes and62 working helper contexts. Source golden checks rejected all6 no-op, partial, mode, hook and symlink controls.

The real Amp plugin process also passed a separate fresh-profile test without an account or model: a disposable QA wrapper forwards all62 skill registrations and the tool registration to Amp, then invokes the registered execute callback inside that native process. Assignment, legitimate clarification, literal shell/option inputs,3 invalid-input refusals and recovery all passed. The verifier requires a newly written result and preserves the original installed profile byte-for-byte; an empty exit0 is insufficient. This is callback/registration proof, not connected-thread tool dispatch or model-quality evidence.

This native CLI route does not establish hosted/Puck support or a curated Amp marketplace listing. Public source distribution and any hosted plugin-repository publication remain separate from native acceptance. The adapter adds no hooks, background jobs, MCP servers, provider settings or permission grants.

## Source and limits

All profiles retain 1,196 canonical files from core `ee38d3de3d4b0d5467a589d5cb908f4964f593fe` and the reviewed native source `085ebb9e9c137c5046c2153b9413d9badd102ce7`. The golden verifier rebuilds profiles from that source and rejects a no-op adapter, a changed adapter plus edited supplied manifest, changed modes, unexpected lifecycle hooks and symlinks. Native source/context checks are separate from model activation.

These are isolated host management, public-install, registration and helper checks with **no model calls**. They do not establish model quality, credentialed provider access, a filesystem sandbox, production readiness or absence of all vulnerabilities. Local Python helpers require Python 3.10 or later; individual workflow prerequisites and host permissions apply. The original [validation scope](VALIDATION.md) and [data handling](plugin/DATA-HANDLING.md) still apply.
