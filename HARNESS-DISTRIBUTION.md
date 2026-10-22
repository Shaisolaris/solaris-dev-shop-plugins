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
dsh plugin --profile solaris-test add "git+https://github.com/Shaisolaris/solaris-dev-shop-plugins.git#e38f945bbd969571969dc8e27cc5f9571b2e44f8&path:/harnesses/deepseek"
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

Public Git transport is **not accepted**: the native manager reports installation success for the pinned Git package, but the actual V2 registry returns zero Solaris skills. Adding a root export did not fix this. Local loading passes; public-Git marketplace submission is held until the loading failure is resolved. This prevents installer success from being mistaken for usable runtime behavior.

## Qwen Code

Qwen Code **0.26.0** directly installed the existing public Gemini-format source below, converted its manifest through the native manager, and lists 62 enabled skill entries:

```sh
qwen extensions install https://github.com/Shaisolaris/solaris-dev-shop-gemini --ref 1521695cb8b5bac656c8bdfc1146d53e1fa707de
```

All1975 installed source files and executable modes match the public revision; all62 context calls and the installed coordinator pass outside the checkout. This uses the host's documented cross-format support, with the complete source and resources retained. It is not an independent Qwen directory approval.

## Pi

The repository-root `package.json` is a native Pi package manifest. It declares the 62 exact skill files from the existing contained profile; it declares no extensions, prompts or themes. Pi **1.4.0** installed the local package, then its public native package resolver and skill loader found all 62 unique names with no diagnostics. The actual public Git install at `e38f945bbd969571969dc8e27cc5f9571b2e44f8` also passes all62 names through the native manager and loader. All1973 contained payload file bytes/modes match; all62 live context calls and the installed coordinator work outside the checkout. The Pi gallery indexes npm packages; npm publisher authentication is a separate unresolved requirement.

## Source and limits

All profiles retain 1,196 canonical files from core `ee38d3de3d4b0d5467a589d5cb908f4964f593fe` and the reviewed native source `085ebb9e9c137c5046c2153b9413d9badd102ce7`. The golden verifier rebuilds profiles from that source and rejects a no-op adapter, a changed adapter plus edited supplied manifest, changed modes, unexpected lifecycle hooks and symlinks. Native source/context checks are separate from model activation.

These are isolated host management, public-install, registration and helper checks with **no model calls**. They do not establish model quality, credentialed provider access, a filesystem sandbox, production readiness or absence of all vulnerabilities. Local Python helpers require Python 3.10 or later; individual workflow prerequisites and host permissions apply. The original [validation scope](VALIDATION.md) and [data handling](plugin/DATA-HANDLING.md) still apply.
