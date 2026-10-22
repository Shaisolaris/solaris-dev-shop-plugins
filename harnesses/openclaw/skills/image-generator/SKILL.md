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

Load the [Solaris workflow](resources/canonical/employees/creative-media/image-generator/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
