# OpenAI listing correction for 0.63.0

The public release remains immutable. The submission ZIP applies two listing
changes to the independently checked release ZIP:

- Shorten the subtitle to `61 specialist workflows` (23 characters).
- Link the already-published MIT software license as the software terms. This
  does not apply the separate website-use restrictions to the open-source code.

`tools/prepare_openai_submission.py` pins the exact base ZIP hash, preserves the
version, copies ZIP member metadata, changes only the listing manifest and its
explicit overlay provenance, and writes a complete member-hash receipt. All
canonical source, workflow adapters, assets and runtime code remain identical.
The original distribution verifier establishes the base artifact; the overlay
receipt and independent byte comparison establish this bounded correction.
Do not claim the unchanged base packager directly generated the corrected ZIP.

```sh
python3 tools/prepare_openai_submission.py \
  --base-zip /absolute/path/to/released/solaris-dev-shop-0.63.0-plugin.zip \
  --output-dir /absolute/path/to/a/fresh/submission-directory
```

A correct package is separate from directory eligibility. Keep
`requires_local_executor: true`. The current portal restriction on additional
skills-only submissions requires an eligibility decision from OpenAI; a dummy
MCP server or a claim of partner approval is not a resolution. Local MCP
submissions additionally require OpenAI partner approval and organization
allowlisting. See the [official desktop submission instructions](https://developers.openai.com/plugins/deploy/desktop-only).
