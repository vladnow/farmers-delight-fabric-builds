# Source-build preparation — 2026-10-06

- Included existing Farmer's Delight Refabricated Fabric sources for Minecraft 26.2 and 26.3 with exact upstream commit references.
- Retained original Java code, assets, recipes and attribution.
- Pinned Fabric Loom to the locally resolved stable version 1.17.21 and recorded the Gradle 9.6.1 distribution SHA-256.
- Declared Java 25 as a loader dependency in local builds.
- Moved GhostSlotsInvoker and GuiGraphicsExtractorAccessor to the client mixin list so dedicated servers do not attempt to load their client-only targets.
- Bundled full license texts for third-party source files in local binary and source JARs.
- Removed upstream Modrinth, CurseForge and Maven publishing configuration.
- Added Windows build helper, GitHub Actions build matrix, bilingual publication drafts and publication conditions.

See `verification/TEST-REPORT.md` for validation and runtime-test limits.
