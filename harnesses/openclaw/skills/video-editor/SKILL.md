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

Load the [canonical workflow](../../employees/creative-media/video-editor/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
