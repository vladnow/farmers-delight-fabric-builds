# Release notes

These are notes for source-built copies of existing upstream releases. Separate Modrinth reuploads require explicit permission; see `../PUBLISHING.ru.md`. Do not call these newly developed ports.

## Minecraft 26.2 — Farmer's Delight Refabricated 3.6.26

- Fabric build from upstream commit `f55a773870197eaed490ae381f82fc0a56907989`.
- Java 25; verified with Fabric Loader 0.19.3 and Fabric API 0.157.0+26.2.
- Original mod functionality and assets retained.
- Local source preparation pins Loom 1.17.21, adds a Gradle distribution checksum, declares Java 25 in mod metadata and bundles third-party license texts.
- Two client-only accessors are now in the client mixin list, removing their missing-target warnings on dedicated servers.
- Original publishing integrations have been removed from the prepared source projects.
- Full build and verification status: `../verification/TEST-REPORT.md`.

## Minecraft 26.3 — Farmer's Delight Refabricated 3.6.27

- Fabric build from upstream commit `615259dd453adec97b045765566a8f982b79cd71`.
- Java 25; verified with Fabric Loader 0.19.5 and Fabric API 0.160.4+26.3.
- Same source-preparation changes as the 26.2 build.
- This commit is the current 26.3 branch snapshot obtained on October 6, 2026, rather than a claim of a byte-identical rebuild of the earlier published JAR.
- Full build and verification status: `../verification/TEST-REPORT.md`.
