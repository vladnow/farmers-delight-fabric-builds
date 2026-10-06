# Farmer's Delight — Fabric source builds

Source and build preparation for the existing **Farmer's Delight Refabricated** port on Minecraft **26.2** and **26.3**. This is an unofficial source-build collection. The original mod is by **vectorwing**; the Fabric port is maintained by **MehVahdJukaar, ChrysanthCow and cassiancc**, with additional upstream contributors. This collection does not claim authorship of the mod or of its Fabric port.

Repository: https://github.com/vladnow/farmers-delight-fabric-builds

Prepared downloads: https://github.com/vladnow/farmers-delight-fabric-builds/releases

## Versions

| Minecraft | Fabric port | Minimum loader used for verification | Fabric API |
| --- | --- | --- | --- |
| 26.2 | 3.6.26 | 0.19.3 | 0.157.0+26.2 |
| 26.3 | 3.6.27 | 0.19.5 | 0.160.4+26.3 |

Use **Java 25**. Both client and server need the mod and Fabric API. Recipe viewers and configuration screens are optional. Only install one mod with the ID `farmersdelight` in a game instance.

## Install

Use the JAR files for your exact Minecraft version from `dist/26.2` or `dist/26.3`. Each directory includes a checksum-verified upstream mod JAR and the Fabric API version listed above. Files in a `local-build` subdirectory are built here from the included sources; choose either that mod JAR or the upstream mod JAR. A `-sources.jar` is for developers and must not be installed as the mod.

Install Fabric Loader, then put the mod and Fabric API in the instance's `mods` directory. The same files are needed on a Fabric server. See `verification/TEST-REPORT.md` for the precise extent of local verification.

## Build

Each `fabric-26.x` directory is an independent Gradle project. On Windows, from this directory:

```powershell
./build.ps1 -Minecraft all -JavaHome 'C:/path/to/jdk-25'
```

The prepared workspace also has a portable JDK in `.tools`; `build.ps1` can discover it automatically when `JAVA_HOME` is unset. It is excluded from the source archive. Builds need internet access to download dependencies.

On Linux/macOS with JDK 25:

```sh
cd fabric-26.2
chmod +x gradlew
./gradlew build --no-daemon
```

Repeat in `fabric-26.3` for Minecraft 26.3. Outputs are in each project's `build/libs`.

## GitHub

Unpack `farmers-delight-fabric-sources.zip` into an empty directory and upload its contents to a new repository, for example `farmers-delight-fabric-builds`. The archive includes both complete source projects, licenses, provenance and a GitHub Actions build matrix. It excludes nested Git repositories, downloaded tools, caches and binary game files. The original local checkouts retain Git metadata for the pinned upstream snapshots.

When uploading many files, use Git or GitHub Desktop rather than the browser's file uploader. Create an empty repository and upload the unpacked source tree. When adding a release, attach the corresponding source ZIP alongside binary downloads to preserve access to the included third-party sources.

CI builds both versions and attaches JAR artifacts. It does not publish to Modrinth or CurseForge. Keep the attribution, licenses and source files when distributing builds. The upstream commits and original release IDs are recorded in `verification/provenance.json`.

## Publication and naming

Read `PUBLISHING.ru.md` before uploading a separate Modrinth project. MIT permits modification and redistribution while retaining notices; third-party files have additional licenses. A direct reupload of an existing port needs author permission under Modrinth's rules. This collection does not introduce a substantial gameplay fork.

Use a clearly distinguished repository name and describe it as an unofficial source build. No permission to present this collection as the official project, or to use an author's name as your own identity, is implied.

## Upstream

- Original: https://github.com/vectorwing/FarmersDelight
- Fabric sources: https://github.com/MehVahdJukaar/FarmersDelightRefabricated
- Existing Fabric releases: https://modrinth.com/mod/farmers-delight-refabricated

## По-русски

Здесь подготовлены исходники существующего Fabric-порта для 26.2 и 26.3, готовые файлы мода и инструкции для GitHub. Для установки открой `dist` и выбери папку своей версии. Установи Fabric Loader, затем положи JAR мода и Fabric API в `mods`. Сборку исходников запускает `build.ps1`. Условия отдельной публикации и использования названия описаны в `PUBLISHING.ru.md`; результаты проверок — в `verification/TEST-REPORT.md`.
