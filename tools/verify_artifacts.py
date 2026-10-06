"""Verify archive contents and upstream hashes without launching Minecraft."""
import hashlib
import json
import struct
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def sha(path, algorithm):
    with path.open('rb') as file:
        return hashlib.file_digest(file, algorithm).hexdigest()


def gameplay_tree(project):
    files = []
    for directory in ('src/main/java', 'src/generated', 'src/main/resources/assets', 'src/main/resources/data'):
        files.extend(file for file in (project / directory).rglob('*') if file.is_file())
    digest = hashlib.sha256()
    for file in sorted(files, key=lambda file: file.relative_to(project).as_posix()):
        digest.update(file.relative_to(project).as_posix().encode('utf-8') + b'\0')
        # Git may check textual source files out with LF or CRLF.
        data = file.read_bytes()
        if file.suffix in ('.java', '.json', '.mcmeta', '.txt'):
            data = data.replace(b'\r\n', b'\n')
        digest.update(hashlib.sha256(data).digest())
    return {'file_count': len(files), 'sha256': digest.hexdigest()}


def inspect_mod(path, game, require_notices):
    with ZipFile(path) as jar:
        assert jar.testzip() is None, f'Corrupt ZIP: {path}'
        names = set(jar.namelist())
        metadata = json.loads(jar.read('fabric.mod.json'))
        assert metadata['id'] == 'farmersdelight'
        assert metadata['version'].startswith(game + '-')
        assert metadata['depends']['minecraft'] == '~' + game
        assert 'fabric-api' in metadata['depends']
        assert 'LICENSE_FarmersDelight' in names
        assert 'icon.png' in names
        if require_notices:
            assert metadata['depends']['java'] == '>=25'
            for license_name in ('LGPL-2.1.txt', 'Blu-License.txt'):
                assert 'META-INF/licenses/' + license_name in names
        for entries in metadata['entrypoints'].values():
            for entry in entries:
                entry = entry if isinstance(entry, str) else entry['value']
                assert entry.replace('.', '/') + '.class' in names, entry
        mixins = json.loads(jar.read('farmersdelight.mixins.json'))
        for name in mixins.get('mixins', []) + mixins.get('client', []):
            class_name = mixins['package'] + '.' + name
            assert class_name.replace('.', '/') + '.class' in names, class_name
        assert metadata['accessWidener'] in names
        classes = [name for name in names if name.endswith('.class')]
        majors = set()
        for name in classes:
            data = jar.read(name)
            assert data[:4] == b'\xca\xfe\xba\xbe', name
            majors.add(struct.unpack('>H', data[6:8])[0])
        assert majors == {69}, f'Expected Java 25 class files: {majors}'
        json_count = 0
        for name in names:
            if name.endswith('.json'):
                json.loads(jar.read(name))
                json_count += 1
        return {
            'file': str(path.relative_to(ROOT)).replace('\\', '/'),
            'version': metadata['version'],
            'sha256': sha(path, 'sha256'),
            'class_count': len(classes),
            'class_major_versions': sorted(majors),
            'json_count': json_count,
            'mixin_count': len(mixins.get('mixins', [])) + len(mixins.get('client', [])),
            'entrypoints_and_mixins_present': True,
            'archive_crc_valid': True,
        }


def main():
    report = {'minecraft': {}}
    for game in ('26.2', '26.3'):
        release = json.loads((ROOT / 'verification' / f'upstream-{game}.json').read_text(encoding='utf-8-sig'))
        primary = next(file for file in release['files'] if file['primary'])
        upstream = ROOT / 'dist' / game / primary['filename']
        assert sha(upstream, 'sha512') == primary['hashes']['sha512']
        api = json.loads((ROOT / 'verification' / f'fabric-api-{game}.json').read_text(encoding='utf-8-sig'))
        api_file = next(file for file in api['files'] if file['primary'])
        api_path = ROOT / 'dist' / game / api_file['filename']
        assert sha(api_path, 'sha512') == api_file['hashes']['sha512']
        with ZipFile(api_path) as jar:
            assert jar.testzip() is None
            assert json.loads(jar.read('fabric.mod.json'))['id'] == 'fabric-api'
        local_dir = ROOT / 'dist' / game / 'local-build'
        local = next(file for file in local_dir.glob('*.jar') if not file.name.endswith('-sources.jar'))
        source_jar = next(local_dir.glob('*-sources.jar'))
        with ZipFile(source_jar) as jar:
            assert jar.testzip() is None
            assert 'LICENSE' in jar.namelist()
            for license_name in ('LGPL-2.1.txt', 'Blu-License.txt'):
                assert 'META-INF/licenses/' + license_name in jar.namelist()
        project = ROOT / f'fabric-{game}'
        baseline = json.loads((ROOT / 'verification' / 'source-baseline.json').read_text(encoding='utf-8'))
        assert gameplay_tree(project) == baseline[game], f'Gameplay sources/assets differ from the recorded upstream tree: {game}'
        report['minecraft'][game] = {
            'upstream': inspect_mod(upstream, game, False),
            'local_build': inspect_mod(local, game, True),
            'upstream_sha512_matches_modrinth': True,
            'fabric_api_sha512_matches_modrinth': True,
            'java_sources_and_game_assets_unchanged': True,
            'source_jar_sha256': sha(source_jar, 'sha256'),
            'fabric_api_sha256': sha(api_path, 'sha256'),
        }
    (ROOT / 'verification' / 'artifact-checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    for game, data in report['minecraft'].items():
        print(f"{game}: OK; {data['local_build']['class_count']} classes, {data['local_build']['json_count']} JSON files, {data['local_build']['mixin_count']} mixins")


if __name__ == '__main__':
    main()
