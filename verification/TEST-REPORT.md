# Verification report — 2026-10-06

## Result

Both prepared Fabric source projects build successfully with JDK 25.0.4.1, Gradle 9.6.1 and Loom 1.17.21. Both local mod JARs pass dedicated-server initialization with their matching Minecraft/Fabric versions. This is a build and initialization check, not a complete gameplay or graphical-client test.

| Minecraft | Mod | Loader | Fabric API | Build | Server initialization |
| --- | --- | --- | --- | --- | --- |
| 26.2 | 3.6.26+refabricated | 0.19.3 | 0.157.0+26.2 | Passed | Passed |
| 26.3 | 3.6.27+refabricated | 0.19.5 | 0.160.4+26.3 | Passed | Passed |

## What was checked

- The full `build` task completed for both final prepared projects. Java compilation, resource processing, binary and source JAR creation succeeded. Loom's access-widener validation passed.
- The upstream projects have no unit test source set contents; Gradle reports `test NO-SOURCE`. No unit-test coverage is claimed.
- Production Fabric servers were prepared in isolated local directories, using only the matching local mod JAR and Fabric API. Each ran `--initSettings --nogui`, loaded the mod configuration and initialized server settings with exit code 0.
- Initial runs exposed two client-only mixins in the common mixin list. GhostSlotsInvoker and GuiGraphicsExtractorAccessor were moved to the client list in both projects. Final runs have no missing-target warnings for those mixins.
- The mod and Fabric API downloads match the SHA-512 hashes supplied by Modrinth. Binary and source ZIP CRCs are valid. Local builds contain the original license plus full third-party license texts.
- All bundled JSON files parse successfully: 1,925 in the 26.2 mod JAR and 1,944 in the 26.3 mod JAR.
- All declared entrypoints and mixin classes are present: 38 mixins for 26.2 and 37 for 26.3. Compiled classes use Java 25 class-file version 69: 374 classes for 26.2 and 372 for 26.3.
- Java sources, generated game resources, assets and data were checked against the unmodified upstream Git snapshots. Their normalized tree hashes are recorded in `source-baseline.json`; they are unchanged. Only packaging, metadata and client/server mixin selection were adjusted.
- Source and installation archives are checked for required files, CRC validity and exclusion of embedded Git repositories, caches, JDK and Minecraft server binaries.
- Both projects were extracted from the source ZIP into a fresh directory and successfully rebuilt from scratch with `build --offline`, using the downloaded dependency cache. Both clean archive builds completed in 27 seconds. The source archive contains 5,633 files before the final documentation/patch additions; only Gradle wrapper JARs are included as binary build tools.

Machine-readable details: `artifact-checks.json`, `provenance.json`, `source-baseline.json` and the workspace root `SHA256SUMS.txt`. `local-changes-26.x.patch` records tracked changes to each upstream snapshot; added license files are also included in each project.

## Limits and remaining manual validation

- The graphical client was not launched. Rendering, kitchen screens, recipe-book interaction and optional recipe/configuration integrations have not been tested locally.
- `--initSettings` exits before loading or generating a playable world. Cooking, cutting, planting, world generation, multiplayer interaction and saved-world migrations have not been exercised.
- Minecraft EULA acceptance was not enabled in the test directories. Test directories contain `eula=false` and no generated world. No public test server was opened.
- The host's Windows performance-counter registry produced OSHI diagnostics during startup. Startup continued successfully; the operating-system registry was not modified. Java native-access/deprecation warnings and Gradle deprecation warnings also remain.
- This report covers local verification. See the repository's Actions and Releases pages for remote CI and publication status. No Modrinth or CurseForge publication is part of these checks.
- The 26.3 source snapshot is a branch commit dated September 26, 2026. Its version label matches upstream 3.6.27; byte-identical reproduction of the Modrinth JAR published earlier is not asserted. Local packaging changes also make both local JARs different from the upstream downloads.

Local detailed logs are in this workspace's `verification/build-final.log` and `verification/server-init-final-26.x.log`; logs with host paths are excluded from the public source archive.

Before a public binary release, manually launch a client and a world for each version, check a cooking-pot recipe, a cutting-board recipe, crop growth, rich soil, rope and the recipe book, and validate any optional integrations you intend to advertise.

## По-русски

Сборка и начальная загрузка серверной части прошли для обеих версий. Контрольные суммы, содержимое архивов, лицензии, JSON и наличие нужных классов проверены. Это не подтверждение проверки всех механик в игре: графический клиент и игровой мир здесь не запускались. Условия отдельной публикации на Modrinth находятся в `../PUBLISHING.ru.md`.
