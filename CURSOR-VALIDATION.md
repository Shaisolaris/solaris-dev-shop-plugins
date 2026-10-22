# Cursor native-host validation

Version **0.63.0**. **61 specialist employees + chief-of-staff coordinator = 62 workflows.**
No new employee capability or release-version bump is introduced by this catalog.

## Exact candidate

The plugin is the existing portable Agent Plugins profile at `copilot/plugin`,
reviewed at [085ebb9e9c137c5046c2153b9413d9badd102ce7](https://github.com/Shaisolaris/solaris-dev-shop-plugins/tree/085ebb9e9c137c5046c2153b9413d9badd102ce7/copilot/plugin).
The canonical core is [ee38d3de3d4b0d5467a589d5cb908f4964f593fe](https://github.com/Shaisolaris/solaris-dev-shop/commit/ee38d3de3d4b0d5467a589d5cb908f4964f593fe).
This catalog change modifies neither plugin profile, canonical runtime, existing tags nor assets.

## Observed checks — October 22, 2026

- Official native Cursor **3.24.18**, macOS arm64, clean application profile.
- The complete profile was loaded through documented `~/.cursor/plugins/local` discovery.
- Native Customize displays installed **Solaris Dev Shop**, **0.63.0**, **Skills 62**.
- All 62 native skill names exactly match the profile; the chief-of-staff skill opens in-app.
- All **1,973 installed file bytes and executable modes** match the immutable source.
- All **1,196 canonical file hashes** match the pinned core provenance.
- All 62 installed Python entrypoints return the expected source/context from outside the checkout.
- The installed coordinator self-test passes and intake assigns `solaris.code-reviewer`.
- A real synthetic SQLite snapshot, damage, dry run and confirmed restore recovers both original rows; a neighboring file remains unchanged.
- The installed wrapper rejects a helper path outside its role and rejects a modified helper, each with exit 2. The original helper is restored byte-for-byte after the control.

The local test ran no model calls and created no new credentials or provider grants.
Local helper commands use Python 3.12. This establishes native component loading
and bounded installed-helper behavior, not model activation/quality, a filesystem
sandbox, Grok Bot cloud import, provider approval or absence of all vulnerabilities.
The existing [validation scope](VALIDATION.md) and [data handling](plugin/DATA-HANDLING.md) apply.

## Reviewer reproduction

1. Check out the exact profile above; retain the whole `copilot/plugin` tree.
2. Copy it to the documented local plugin folder and reload Cursor.
3. Open Customize → Solaris Dev Shop; check version and all 62 workflows.
4. Open `chief-of-staff`; resolve its local entrypoint relative to the skill file.
5. Run `python -B <entrypoint> --context`, then `self-test` and `intake "review this code" --json` from another working directory.
6. Use only disposable synthetic datasets for the documented SQLite recovery drill.

Source: [Cursor plugin discovery and local testing documentation](https://prod.cursor.com/docs/plugins).
Curated marketplace submission and legal acceptance are separate steps.
