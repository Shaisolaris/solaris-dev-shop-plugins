# Solaris Dev Shop native plugin

61 specialist workflows, a chief of staff and executable local helpers. Published by
Solaris Technologies. Generated from [Solaris Dev Shop 0.63](https://github.com/Shaisolaris/solaris-dev-shop/tree/ee38d3de3d4b0d5467a589d5cb908f4964f593fe).

## Install

### Codex

```sh
codex plugin marketplace add Shaisolaris/solaris-dev-shop-plugins
codex plugin add solaris-dev-shop@solaris-technologies
```

### Claude Code

```text
/plugin install solaris-dev-shop --marketplace Shaisolaris/solaris-dev-shop-plugins
```

Or add this repository as a marketplace and install `solaris-dev-shop@solaris-technologies`.

### OpenCode V2

```sh
opencode plugin add 'github:Shaisolaris/solaris-dev-shop-plugins#main::path:plugin'
```

For a pinned installation, replace `main` with the complete distribution commit.
For a local installation, add the extracted `plugin` directory to `plugins` in
`opencode.json`. This adapter uses the V2 API, tested with CLI/SDK 2.1.2.

## Use

Ask the host to use the Solaris chief of staff or a named specialist. The native
skill entry loads the canonical workflow and its companion files. Run helpers
from their canonical role folders. See [the capability guide](docs/capabilities.md)
for runnable examples, and [the unchanged upstream README](SOURCE-README.md).

The source package contains specialist resources. The optional Python wheel
contains the deterministic router and catalog rather than every helper.

## Scope and evidence

The plugin adds no account access, standing tool permissions, telemetry service,
MCP connection or background schedule. The host supplies tools and permissions.
Local helpers retain their documented runtime and operating-system limits.

The 61-role roster is not evidence that every role gained new executable behavior:
the 0.62 programme records changed-role source/runtime evidence for 37 roles.
Examples are bounded local or synthetic workflows, not production certification.
Host discovery and installed-helper execution are checked separately from model
activation. Native format support is separate from curated directory approval.

OpenCode's model/provider configuration is independent of the plugin. No
standalone DeepSeek plugin marketplace approval is claimed.

## Support

Use [GitHub issues](https://github.com/Shaisolaris/solaris-dev-shop-plugins/issues) or email shehryar@solaristek.com.
Do not post credentials, personal data or private source code in public issues.
The software is distributed under the upstream [MIT license](LICENSE).
See [plugin data handling](DATA-HANDLING.md) for local files, host/provider
processing and support contacts. The publisher website policy has its own stated scope.
