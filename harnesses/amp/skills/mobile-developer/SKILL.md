---
name: mobile-developer
description: ⚠️ ALWAYS load `mobile-mcp-operator.md` AND `android-architecture.md`
  FIRST when ANY mobile work begins - these contain canonical mobile-next/mobile-mcp
  tools (cross-platform iOS+Android device automation), Android-Ui-MCP fallback, and
  dpconde NowInAndroid architecture patterns. the coding agent forgets these exist
  and falls back to telling the owner to manually click in Android Studio / Xcode
  if not loaded at session start. Mobile developer for Solaris - native iOS (Swift/SwiftUI),
  native Android (Kotlin/Jetpack Compose), React Native (New Architecture + Hermes
  + TurboModules), Flutter (Dart 3, Impeller, Riverpod/Bloc), Expo SDK 55+, Ionic/Capacitor,
  cross-platform architecture decisions, offline-first sync, push notifications, deep
  linking, biometric auth, ASO, CI/CD (Fastlane + EAS + Bitrise + Codemagic), mobile
  security (OWASP MASVS), platform design (HIG + Material), AR (ARKit + ARCore), on-device
  ML (Core ML + ML Kit), wearables, App Clips / Instant Apps, Live Activities.
---

Load the [Solaris workflow](resources/canonical/employees/engineering/mobile-developer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
