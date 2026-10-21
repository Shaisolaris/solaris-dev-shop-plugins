# Native package validation

The implementation source is pinned to Solaris Dev Shop commit
[`d6f7c37c6039320f2eb284363038edae0cf15e7b`](https://github.com/Shaisolaris/solaris-dev-shop/commit/d6f7c37c6039320f2eb284363038edae0cf15e7b), released as 0.62.
`BUILD.json` and `plugin/SOLARIS-BUILD-SOURCE.json` bind the native payload to that source.

## What was checked

- All 1,196 shipped canonical files match their upstream bytes. The upstream README is preserved as `SOURCE-README.md`; repository `.gitignore` is deliberately omitted. The original 61-role roster and artwork files are preserved.
- All 62 native skill entries resolve to their original workflow files and companion resources. Discovery adapters add no new capability claims.
- Codex CLI 0.163.0-alpha.10.2 installs the package. Its app-server `skills/list` returns all 62 Solaris skills as enabled, with no Solaris discovery errors.
- Claude Code 2.1.306 installs the package and reports 62 skills in its native component inventory. Its strict directory-profile validator reports no findings, warnings or install-instruction advice.
- OpenCode CLI/SDK 2.1.2 loads the native adapter. Its actual authenticated local HTTP API returns all 62 Solaris workflows with contents matching the canonical files. The asynchronous catalog is awaited before acceptance.
- Router self-tests and the 18-case delivery/recovery oracle pass from native installed package resources outside the checkout. Negative controls cover stale or rewritten evidence, missing deliveries, interrupted execution and invalid handoffs.
- Repeated builds produce the same ZIP SHA-256. The verifier rejects a changed helper, missing workflow, dropped workflow index and mismatched source revision.

The upstream [release CI](https://github.com/Shaisolaris/solaris-dev-shop/actions/runs/39686965940) passed all seven jobs. Its full POSIX suite contains 900 tests; macOS reports three explicit skips. Windows runs the documented core, assurance and platform-boundary lane. Those results belong to the pinned upstream source rather than a claim of universal platform support.

## Verification scope

These are native loading, source integrity and helper-runtime checks. They do not
establish model-driven activation quality, provider approval or every role's
performance on real customer work. Claude CLI model authentication was unavailable;
no model invocation is claimed. Raw host catalogs and local account information
are kept out of this public repository.

The publisher website privacy URL exists, but a direct automated fetch returned
HTTP 403 during preparation. Its stated scope is the company website. See
[plugin data handling](plugin/DATA-HANDLING.md) for the local package's behavior;
a provider may request additional privacy information during review.

## Run the conformance checks

```sh
python -m pip install PyYAML==6.0.3
python tools/verify_distribution.py --source /path/to/pinned-upstream-checkout --self-test
```

The native conformance workflow fetches the exact upstream revision, checks source
and metadata, rejects the negative controls, then runs the packaged router and
real delivery/recovery controls from outside the checkout.
