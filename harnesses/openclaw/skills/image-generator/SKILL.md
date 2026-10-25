---
name: image-generator
description: 'Generative image specialist for Solaris - text-to-image, image editing
  (inpaint/outpaint/conversational edit), character + brand consistency, and vector/logo
  generation across the full 2026 model landscape. Primary Gemini 3 Pro Image ("Nano
  Banana Pro"), drafts on Gemini 2.5 Flash Image; alt FLUX.2 (photographic control
  + FLUX Tools inpaint/outpaint + Kontext editing); specialists Recraft V3 (editable
  SVG/logos) and Ideogram 3.0 (text-in-image). Access via Replicate official MCP +
  fal MCP; free local path via ComfyUI + comfyui-mcp-server + FLUX.2[klein]/SDXL with
  ControlNet/IP-Adapter/LoRA. Cost-aware: drafts cheap, finals on the best model.
  Use when the owner says "generate an image", "make an image", "create a picture",
  "logo", "icon", "vector", "SVG", "product shot", "concept art", "character art",
  "thumbnail image", "inpaint", "outpaint", "remove background", "edit this image",
  "make a variation", "consistent character", "brand style", "Nano Banana", "Gemini
  image", "FLUX", "Recraft", "Ideogram", ".'
---

Load the [canonical workflow](../../employees/creative-media/image-generator/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
