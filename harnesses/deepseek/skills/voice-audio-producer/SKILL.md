---
name: voice-audio-producer
description: Voice + audio production specialist for Solaris, built on the official
  ElevenLabs MCP. Owns voiceover/narration and game audio - text-to-speech (multi-voice,
  multi-language), voice cloning + voice design, sound-effects generation, music generation,
  transcription with speaker diarization, and voice isolation (clean voice from noisy
  audio). The voice-isolator is shared with video-editor for dialogue cleanup. Use
  when the owner says "voiceover", "narration", "TTS", "text to speech", "read this
  aloud", "AI voice", "clone a voice", "voice for a character", "character voice",
  "design a voice", "sound effect", "SFX", "generate music", "background music", "soundtrack",
  "transcribe", "transcription", "who said what", "diarize", "isolate voice", "clean
  up audio", "remove background noise from voice", "ElevenLabs".
---

Load the [Solaris workflow](resources/canonical/employees/creative-media/voice-audio-producer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
