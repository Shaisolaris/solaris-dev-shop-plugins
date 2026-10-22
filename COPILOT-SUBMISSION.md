# GitHub Copilot marketplace candidate

The submission is [Awesome Copilot issue 5257](https://github.com/github/awesome-copilot/issues/5257). Submission is not marketplace approval.

The original package passed manifest, version and install checks, but its 63 skill-to-shared-file links failed the marketplace's individual skill-directory containment rule. The Copilot variant at `copilot/plugin` retains all 62 workflows and the unchanged pinned canonical runtime. Each skill now contains its workflow/reference mirror and a local executable entrypoint. Resource mirrors satisfy this packaging requirement; they add zero employee capabilities.

Python entrypoints resolve helpers in the original shared role folder, preserve its working directory, refuse role-relative escapes and refuse a helper that differs from the source manifest. The coordinator entrypoint runs the real shared routing engine. These checks do not grant permissions or provide a security sandbox.

The base package remains at `plugin` for the existing native distributions. Its source revision, release versions, tags and assets are unchanged. `SOLARIS-BUILD-SOURCE.json` binds the canonical runtime. The variant's `COPILOT-LAYOUT.json` records every mirrored source hash and entrypoint hash. Four Markdown-like strings inside existing code examples are explicitly recorded as excluded patterns; no unrecognized missing reference is silently ignored.

Validation: the exact marketplace lint dependency, `@microsoft/vally@0.18.0`, passes all 62 workflows locally. Negative controls still reject a link outside its skill and a missing contained workflow. Copilot CLI 1.0.102 installed the prototype with 62 native workflows, no duplicate native workflows, and matching bytes/modes for all 1,973 payload files. The installed coordinator returned a real code-review assignment. A separate fixture restored two damaged SQLite rows through the new role entrypoint and retained neighboring data. Final candidate byte equality and these runtime checks are required in CI before updating the submission's immutable SHA.

No model activation, provider approval or improved performance for every role is claimed. No source implementation, account permission, lifecycle hook or release version is changed by this layout.

```sh
python tools/verify_copilot_layout.py --self-test
```


The current metadata repair preserves the original notice at `SOURCE-NOTICE.md`, credits the byte-identical contained upstream-license copy in `NOTICE.md`, and retains the source repository's CI snapshots as inert data under `source-config/.github`. All1196 canonical file bytes remain bound through the declared path map. The contained profile now has1974 files. Actual composite G38 provenance and G42 cross-checks are required alongside native installation checks; source-core tests with repository-specific declaration counts are retained unchanged as source data.
