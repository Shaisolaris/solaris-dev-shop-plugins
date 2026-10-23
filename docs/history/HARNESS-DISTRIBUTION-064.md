# Solaris native distributions 0.64.0

**61 specialist employees and one chief-of-staff coordinator: 62 workflows.**

All current profiles preserve 1,197 canonical files from core [`3a577e42`](https://github.com/Shaisolaris/solaris-dev-shop/commit/3a577e42c48473f6ef8680950dd55c067820d5d3). The immutable tested distribution source is [`2e51c951`](https://github.com/Shaisolaris/solaris-dev-shop-plugins/commit/2e51c951ce4573c0ab7c5cc807118d6e0c5b815c). Adapters add native loading and local entrypoints; they do not represent new capabilities for every specialist. Original branding, source bytes, executable modes, license notices and helper boundaries remain checked.

## Tested hosts

| Host | Actual native evidence | Complete profile files |
|---|---|---:|
| Codex CLI 0.163.0-alpha.11.1 | Public Git installation; app-server discovers 62 enabled workflows; exact payload and coordinator | 1,269 |
| Claude Code 2.1.306 | Public branch observed at the immutable revision; enabled native inventory of 62; exact payload and coordinator | 1,269 |
| OpenCode 2.1.2 | Public Git installation; authenticated local API exposes 62 complete bodies; exact payload and coordinator | 1,269 |
| GitHub Copilot CLI 1.0.102 | Native install and 62 owned workflows; exact contained payload and coordinator | 1,975 |
| Cursor 3.24.18 | Actual app displays 0.64.0 and all 62 workflows; exact payload, helpers and SQLite recovery | 1,975 |
| DeepSeek Harness 0.2.1-rc.2 | Public Git installation; actual provider returns all 62 bodies and resource paths; helpers | 1,974 |
| Kilo 7.8.15 | Public Git V2 API returns all 62 bodies/descriptions/locations; exact payload and helpers on macOS and Linux CI | 1,973 |
| Pi 1.4.0 | Public Git native package resolver/skill loader exposes 62 names/descriptions/paths with no diagnostics; helpers | 1,975 contained |
| Kimi Code 2.3.0 | Authenticated loopback native plugin API installs exact public revision, enabled/state OK/62 skills; helpers | 1,975 contained |
| Factory Droid 0.247.0 | Native Git-subdirectory install; exact contained payload and helpers | 1,975 |
| Gemini CLI 0.65.0 | Native extension install and 62 owned workflows; complete payload and helpers; vendor built-ins counted separately | 1,974 |
| Qwen Code 0.26.0 | Exact public Gemini revision converted by native manager; 62 enabled workflows; exact source and helpers | 1,974 payload |
| OpenClaw 2026.10.5 | Public Git install/enable; 62 visible eligible workflows; exact source and actual intake controls | 1,975 |
| Antigravity CLI 1.4.5 | Fresh hosted Linux install/enable/discovery of 62 workflows; exact payload and helpers | 1,972 |
| Cline CLI 3.0.73 / SDK 0.0.95 | Public Git CLI install; 62 owned skills plus real worker/ContributionRegistry intake execution | 1,974 |
| Amp 0.0.1792680614-g8973a3 | Authenticated stock project discovery; separate actual native-process registration and callback outcomes | 1,974 |

Native discovery, management and local helper evidence does not establish model quality, connected model invocation, a filesystem sandbox or curated marketplace approval. Tests made no model calls. Python helpers require Python 3.10+ and applicable role prerequisites; Cline/Amp helpers also require PyYAML. The host retains its normal permission boundaries.

## Codex, Claude and OpenCode

```sh
codex plugin marketplace add Shaisolaris/solaris-dev-shop-plugins --ref 2e51c951ce4573c0ab7c5cc807118d6e0c5b815c
codex plugin add solaris-dev-shop@solaris-technologies
opencode plugin add 'github:Shaisolaris/solaris-dev-shop-plugins#2e51c951ce4573c0ab7c5cc807118d6e0c5b815c::path:plugin'
```

Claude's `#ref` transport expects a branch or tag, rather than an arbitrary commit SHA. The actual test cloned `codex/native-064`, verified HEAD was exactly `2e51c951`, then installed `solaris-dev-shop@solaris-technologies`. For immutable local testing, check out the exact public revision and add that checkout with `claude plugin marketplace add /absolute/path/to/checkout`; install the same plugin selector. Do not mistake a moving branch for an immutable revision.

## DeepSeek Harness

```sh
dsh plugin --profile solaris add 'git+https://github.com/Shaisolaris/solaris-dev-shop-plugins.git#2e51c951ce4573c0ab7c5cc807118d6e0c5b815c&path:/harnesses/deepseek'
```

The Cordis bundle targets pre-stable DSH 0.2.1-rc.2. The format1 custom index is [markets/deepseek.json](markets/deepseek.json). Custom-index publication is not a DeepSeek endorsement or a claimed DeepSeek-owned marketplace listing. No default public index is shipped by this host.

## Kilo

Keep the package name before `@github:`:

```sh
kilo plugin 'solaris-dev-shop-kilo@github:Shaisolaris/solaris-dev-shop-kilo#cfd9a91b475f7f3ab3f1d815cd959e4b07aaefd2'
```

The native V2 API is the evidence, rather than the legacy `debug skill` catalog. The official catalog cannot currently express this passing named Git syntax; registry publication or vendor guidance is a separate requirement. See [the existing V2 issue](https://github.com/Kilo-Org/kilocode/issues/15307). No npm policy is weakened to force an unsupported transport.

## Pi, Kimi and Factory

```sh
pi install git:github.com/Shaisolaris/solaris-dev-shop-plugins@2e51c951ce4573c0ab7c5cc807118d6e0c5b815c
```

Pi's root manifest names 62 exact contained skill files and declares no extensions, prompts or themes. Its npm-indexed gallery requires a separate registry upload. Kimi's root `kimi.plugin.json` names 62 contained skill directories and declares no hooks, MCP servers or agents; install the full repository through Kimi's native plugin UI at the exact revision. Factory's actual native catalog/git-subdirectory test used `copilot/plugin` at the same public revision. Factory renames `.claude-plugin` to `.factory-plugin`; its verifier accounts for exactly that host transformation. No Factory model activation is inferred from install/list.

## Gemini and Qwen

The complete native source is [`solaris-dev-shop-gemini@2f9a29a9`](https://github.com/Shaisolaris/solaris-dev-shop-gemini/commit/2f9a29a9d41da0a4d60c9ff7bea9c7aff737a189). Gemini uses its native extension format. Qwen directly accepts that Gemini format:

```sh
qwen extensions install https://github.com/Shaisolaris/solaris-dev-shop-gemini --ref 2f9a29a9d41da0a4d60c9ff7bea9c7aff737a189
```

Qwen preserves all 1,974 payload files plus the four repository publication files and adds exactly two native conversion/install records. Its actual manager lists all 62 workflows enabled for user and workspace. This is cross-format host support, not independent directory approval.

## OpenClaw

```sh
openclaw plugins install git:github.com/Shaisolaris/solaris-dev-shop-openclaw@9194a847a32ffd86f31946da152cde1ad9b0cfdf
openclaw plugins enable solaris-dev-shop
openclaw solaris intake 'review this code' --json
```

Use the normal reviewed-source confirmation. This is a source plugin with a real native intake command, not an opaque executable. Intake returns an assignment without performing specialist work. It uses argument separation, no shell, a 32KiB UTF-8 limit, a 20-second timeout and a minimal child environment. Literal shell/option text, oversized input and recovery were checked. Git installs retain host-owned Git metadata and add a dependency-free lockfile; those exact additions are verified separately from the 1,975 unchanged product files.

The catalog icon is losslessly recompressed below 512KiB; every original RGBA pixel, dimension and colour metadata remains identical. The older ClawHub 0.63 community listing and Review advisory remain historical. A corrected source or new upload does not silently clear that old advisory. Registry publication and its actual new scan are separate gates.

## Antigravity

The strict native profile is public at [`solaris-dev-shop-antigravity@61eef051`](https://github.com/Shaisolaris/solaris-dev-shop-antigravity/commit/61eef051f66d8133b45e04b35b0fa42fdc04e757). Install the complete GitHub-root plugin or use the host's documented `.agents/plugins/` workspace folder. Its strict root manifest permits `name` and `description`; see [the format-specific provenance limitation](ANTIGRAVITY-DISTRIBUTION.md). Google's application receipt is not acceptance. The retired worker and existing Google account were not used for native CI.

## Cline and Amp

```sh
cline plugin install 'https://github.com/Shaisolaris/solaris-dev-shop-cline.git@7d884ae7187b290024956b4a8013937672b22977'
```

Cline CLI/SDK/Kanban loads 62 owned skill bodies/descriptions/paths and executes `solaris_intake` through its real worker and ContributionRegistry. VSCode/JetBrains support is not claimed. Its installer may remove exactly two optional SDK peer-dependency fields; the remaining 1,973 file bytes and every mode are exact. Git metadata is bound to the requested public SHA/origin; only sample hooks are accepted. The native tool passed assignment, legitimate clarification, literal shell/option inputs, three invalid-input refusals and recovery. No `allow-git`/remote policy override is used.

Amp uses a project directory plugin. Clone the complete [`solaris-dev-shop-amp@abdf618c`](https://github.com/Shaisolaris/solaris-dev-shop-amp/commit/abdf618c18c371daa7c9579d72c8e022fe1b3818) into `.amp/plugins/solaris-dev-shop` and check out that exact commit. Stock authenticated discovery returns 62 qualified names/descriptions/paths. A separate disposable QA wrapper forwards the actual native registration APIs and invokes the registered callback inside Amp's real plugin process; assignment, clarification, refusal and recovery passed. This does not claim connected-thread dispatch, hosted/Puck support or a curated Amp listing.

## Verification and publication

See [VALIDATION.md](VALIDATION.md), [Cursor evidence](CURSOR-VALIDATION.md) and [data handling](plugin/DATA-HANDLING.md). Golden rebuilds reject no-op adapters, a changed adapter plus edited submitted manifest, changed modes, unexpected hooks, symlinks and unfinished pre-notice input masquerading as a final distribution. Notices are applied exactly once; source CI snapshots are retained as inert data under `source-config/.github`.

Official catalog requests remain vendor decisions: [OpenCode58104](https://github.com/anomalyco/opencode/pull/58104), [Factory64](https://github.com/Factory-AI/factory-plugins/pull/64), [Kimi4344](https://github.com/MoonshotAI/kimi-code/issues/4344), [Copilot5257](https://github.com/github/awesome-copilot/issues/5257). Hermes admission remains held by its actual scanner; no override or catalog-approval claim is used. Historical 0.63 evidence is retained under [docs/history](docs/history/). Existing release tags and assets are never overwritten.
