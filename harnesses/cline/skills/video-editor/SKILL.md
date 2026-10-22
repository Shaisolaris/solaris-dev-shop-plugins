---
name: video-editor
description: 'Video Editor - FFmpeg-based video editing operations (per opheliabm/the
  coding agent-videoedit gap-fill repo: trimming + cutting + splitting + concatenation
  + speed changes + cropping + scaling + rotation + overlays + picture-in-picture
  + green screen removal + video stabilization + transitions + fades + privacy blur
  + LUT color grading + motion tracking text), audio operations (extraction, normalization,
  denoise, voiceover sync, music ducking), captions + subtitles (SRT/VTT generation,
  burn-in, auto-transcribe via Whisper + AssemblyAI + Deepgram), video formats + codecs
  (H.264, H.265/HEVC, AV1, ProRes, DNxHR), platform-specific exports (YouTube 4K +
  Shorts vertical, Instagram Reels, TikTok, LinkedIn native, Twitter/X), GPU acceleration
  (NVENC, QuickSync, VideoToolbox), batch processing, lossless editing where possible,
  frame-accurate trimming when needed, scene detection (PySceneDetect for auto-cuts),
  color grading (LUT application, color correction, exposure adjustment), b-roll integration,
  J-cut.'
---

Load the [Solaris workflow](resources/canonical/employees/creative-media/video-editor/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
