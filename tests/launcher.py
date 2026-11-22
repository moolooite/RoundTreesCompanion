"""Bare-bones Minecraft launcher for the launch tests.

Reads a launcher profile (vanilla, Fabric, Quilt, Forge or NeoForge), downloads whatever is
missing and works out the command line that starts the client.
"""
import concurrent.futures
import json
import os
import urllib.request
import zipfile


def java(major):
    home = os.environ.get('JAVA%d_HOME' % major) or '/usr/lib/jvm/java-%d-openjdk-amd64' % major
    return os.path.join(home, 'bin', 'java')


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'roundtreescompanion-tests'})
            with urllib.request.urlopen(request, timeout=120) as response, open(dest + '.part', 'wb') as out:
                out.write(response.read())
            os.replace(dest + '.part', dest)
            return dest
        except OSError:
            if attempt == 3:
                raise


def _profile(root, version):
    path = os.path.join(root, 'versions', version, version + '.json')
    if not os.path.exists(path):
        # not installed by a loader, so it has to be a vanilla version
        manifest = fetch('https://piston-meta.mojang.com/mc/game/version_manifest_v2.json',
                         os.path.join(root, 'version_manifest_v2.json'))
        url = [v['url'] for v in json.load(open(manifest))['versions'] if v['id'] == version][0]
        fetch(url, path)
    return json.load(open(path))


def _allowed(rules):
    if not rules:
        return True
    allowed = False
    for rule in rules:
        matches = 'features' not in rule
        system = rule.get('os', {})
        if system.get('name', 'linux') != 'linux' or system.get('arch', 'x86_64') not in ('x86_64', 'amd64'):
            matches = False
        if matches:
            allowed = rule['action'] == 'allow'
    return allowed


def _maven_path(name):
    coords, _, extension = name.partition('@')
    parts = coords.split(':')
    classifier = '-' + parts[3] if len(parts) > 3 else ''
    return '%s/%s/%s/%s-%s%s.%s' % (parts[0].replace('.', '/'), parts[1], parts[2], parts[1], parts[2],
                                    classifier, extension or 'jar')


def client_command(root, version, game_dir, jvm_args=(), game_args=()):
    """Command line for the client of an installed profile. Sounds are skipped, there is nothing to play them on."""
    chain = [_profile(root, version)]
    while 'inheritsFrom' in chain[-1]:
        chain.append(_profile(root, chain[-1]['inheritsFrom']))
    vanilla = chain[-1]

    libraries = os.path.join(root, 'libraries')
    natives = os.path.join(root, 'versions', version, 'natives')
    classpath, seen, downloads, native_jars = [], set(), [], []
    for profile in chain:
        for library in profile.get('libraries', []):
            if not _allowed(library.get('rules')):
                continue
            parts = library['name'].split('@')[0].split(':')
            key = ':'.join(parts[:2] + parts[3:4])
            artifact = library.get('downloads', {}).get('artifact')
            if artifact or 'downloads' not in library:
                if artifact:
                    path, url = artifact.get('path') or _maven_path(library['name']), artifact.get('url')
                else:
                    path = _maven_path(library['name'])
                    url = library.get('url', 'https://libraries.minecraft.net/').rstrip('/') + '/' + path
                # a loader's copy of a library wins over the game's
                if key not in seen:
                    seen.add(key)
                    if url:
                        downloads.append((url, os.path.join(libraries, path)))
                    classpath.append(os.path.join(libraries, path))
            native = library.get('natives', {}).get('linux')
            if native:
                classifier = library['downloads']['classifiers'][native]
                downloads.append((classifier['url'], os.path.join(libraries, classifier['path'])))
                native_jars.append(os.path.join(libraries, classifier['path']))

    # Forge and NeoForge put their own patched copy of the game on the module path
    client = os.path.join(root, 'versions', vanilla['id'], vanilla['id'] + '.jar')
    downloads.append((vanilla['downloads']['client']['url'], client))
    if not any('forge' in profile['id'].lower() for profile in chain[:-1]):
        classpath.append(client)

    index_id = vanilla['assetIndex']['id']
    index = fetch(vanilla['assetIndex']['url'], os.path.join(root, 'assets', 'indexes', index_id + '.json'))
    for name, entry in json.load(open(index))['objects'].items():
        if not name.endswith('.ogg'):
            digest = entry['hash']
            downloads.append(('https://resources.download.minecraft.net/%s/%s' % (digest[:2], digest),
                              os.path.join(root, 'assets', 'objects', digest[:2], digest)))

    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        list(pool.map(lambda download: fetch(*download), downloads))

    os.makedirs(natives, exist_ok=True)
    for jar in native_jars:
        with zipfile.ZipFile(jar) as archive:
            for name in archive.namelist():
                if name.endswith('.so'):
                    archive.extract(name, natives)

    values = {
        'natives_directory': natives, 'launcher_name': 'tests', 'launcher_version': '1',
        'classpath': os.pathsep.join(classpath), 'classpath_separator': os.pathsep,
        'library_directory': libraries, 'version_name': version, 'version_type': 'release',
        'game_directory': game_dir, 'assets_root': os.path.join(root, 'assets'), 'assets_index_name': index_id,
        'auth_player_name': 'Tester', 'auth_uuid': '0' * 32, 'auth_access_token': '0', 'auth_xuid': '0',
        'clientid': '0', 'user_type': 'legacy', 'user_properties': '{}',
    }

    def expand(arguments):
        expanded = []
        for argument in arguments:
            if isinstance(argument, dict):
                if not _allowed(argument.get('rules')):
                    continue
                argument = argument['value']
            for text in argument if isinstance(argument, list) else [argument]:
                for key, value in values.items():
                    text = text.replace('${%s}' % key, value)
                expanded.append(text)
        return expanded

    jvm, game = [], []
    for profile in reversed(chain):
        jvm += expand(profile.get('arguments', {}).get('jvm', []))
        game += expand(profile.get('arguments', {}).get('game', []))
    major = max(vanilla.get('javaVersion', {}).get('majorVersion', 17), 17)
    return [java(major), '-Xmx2G'] + list(jvm_args) + jvm + [chain[0]['mainClass']] + game + list(game_args)
