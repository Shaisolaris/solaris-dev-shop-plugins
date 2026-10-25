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

Load the [canonical workflow](../../employees/engineering/mobile-developer/SKILL.md) and its companion resources. Resolve links relative to this SKILL.md; canonical resources are shared within the complete plugin.

For a local Python helper, use the [guarded role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Use `--context` to locate the canonical role folder for other documented tools.

The entrypoint checks helpers against the bundled source manifest; it is not a filesystem or network sandbox. Host permissions and documented runtime prerequisites apply. Loading the workflow does not authorize installation, remote access, credential changes or scheduled work.
