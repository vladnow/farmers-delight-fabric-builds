"""Create uploadable source and install archives, excluding local tools and Git data."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.gradle', '.tools', 'build', 'run', 'logs', '.idea', '.cursor', '.claude', '__pycache__'}


def package():
    archive = ROOT / 'farmers-delight-fabric-sources.zip'
    with ZipFile(archive, 'w', ZIP_DEFLATED, compresslevel=6) as zip_file:
        for file in sorted(ROOT.rglob('*')):
            relative = file.relative_to(ROOT)
            if not file.is_file() or set(relative.parts) & EXCLUDED:
                continue
            if relative.parts[0] == 'dist' or file.suffix in ('.zip', '.log', '.pyc'):
                continue
            if file.name.endswith('-download.json') or file.name == 'SHA256SUMS.txt':
                continue
            zip_file.write(file, relative.as_posix())
    with ZipFile(archive) as zip_file:
        assert zip_file.testzip() is None
        names = set(zip_file.namelist())
        assert '.github/workflows/build.yml' in names
        for game in ('26.2', '26.3'):
            prefix = 'fabric-' + game + '/'
            for file in ('gradlew', 'gradlew.bat', 'gradle/wrapper/gradle-wrapper.jar', 'build.gradle', 'LICENSE', 'src/main/resources/fabric.mod.json'):
                assert prefix + file in names, prefix + file
            assert any(name.startswith(prefix + 'src/main/java/') for name in names)
            assert any(name.startswith(prefix + 'src/main/resources/assets/') for name in names)
        assert not any(set(Path(name).parts) & EXCLUDED for name in names)
    print(f'Source archive: {archive.name} ({archive.stat().st_size:,} bytes)')
    for game in ('26.2', '26.3'):
        folder = ROOT / 'dist' / game
        mod = next(file for file in (folder / 'local-build').glob('*.jar') if not file.name.endswith('-sources.jar'))
        api = next(folder.glob('fabric-api*.jar'))
        install_archive = ROOT / f'farmers-delight-fabric-{game}-install.zip'
        with ZipFile(install_archive, 'w', ZIP_DEFLATED) as zip_file:
            zip_file.write(mod, 'mods/' + mod.name)
            zip_file.write(api, 'mods/' + api.name)
            zip_file.write(ROOT / 'LICENSE', 'licenses/FarmersDelight-LICENSE.txt')
            for license_file in (ROOT / 'licenses').glob('*.txt'):
                zip_file.write(license_file, 'licenses/' + license_file.name)
            zip_file.writestr('INSTALL.txt', f'Minecraft {game} / Fabric / Java 25\n\nInstall Fabric Loader for Minecraft {game}, then copy both JAR files\nfrom mods/ into your game or server mods/ directory.\nOnly install one implementation with the farmersdelight mod ID.\n\nThis is an unofficial source build of the existing Farmer\'s Delight\nRefabricated port. Original mod: vectorwing. Fabric maintainers:\nMehVahdJukaar, ChrysanthCow, cassiancc and upstream contributors.\n\nCorresponding source: farmers-delight-fabric-sources.zip delivered\nalongside this archive, directory fabric-{game}/.\nUpstream provenance: see verification/provenance.json in that source archive.\n\nBuild and server initialization were verified. Graphical client,\nworld generation and gameplay interactions have not been tested locally.\n\nSource-build differences and publication conditions are in the source\narchive. Separate Modrinth reuploads require author permission.\n')
        with ZipFile(install_archive) as zip_file:
            assert zip_file.testzip() is None
            assert len([name for name in zip_file.namelist() if name.endswith('.jar')]) == 2
        print(f'Install archive: {install_archive.name} ({install_archive.stat().st_size:,} bytes)')
    checksums = []
    files = sorted(ROOT.glob('*.zip')) + sorted((ROOT / 'dist').rglob('*.jar'))
    for file in files:
        with file.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        checksums.append(digest + '  ' + file.relative_to(ROOT).as_posix())
    (ROOT / 'SHA256SUMS.txt').write_text('\n'.join(checksums) + '\n', encoding='utf-8')


if __name__ == '__main__':
    package()
