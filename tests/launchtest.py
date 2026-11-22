#!/usr/bin/env python3
"""Launch tests for the jars in dist/.

A case installs a loader the way the launcher does, starts a dedicated server with the jar in
mods/ (the server also builds a small test world), then joins that world on a client twice,
with and without the jar, and compares the two screenshots.

    tests/launchtest.py                                   every case in tests/cases.txt
    tests/launchtest.py fabric 1.21.1 0.20.1 fabric-1.18.2-1.21.1 [sodium,lithium]

Linux only. Needs Xvfb, xdotool, ImageMagick and JDK 17, 21 and 25, looked up in /usr/lib/jvm
or in JAVA17_HOME, JAVA21_HOME and JAVA25_HOME. Software rendering is enough, 26.3 and up also
want a Vulkan driver (lavapipe works). Everything is kept in run/.
"""
import glob
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.parse

import launcher

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RUN = os.path.join(REPO, 'run')
MINECRAFT = os.path.join(RUN, 'minecraft')

# Rendering mods are client-only, some of them crash a dedicated server
CLIENT_ONLY = re.compile(r'sodium|iris|embeddium|oculus|rubidium')

# Parts of the screenshot that have to differ between the run with the mod and the one without
REGIONS = {'ladders': '320x480+534+0', 'signs and torches': '140x480+310+0', 'sign text': '260x150+30+190'}


def mod_version():
    for line in open(os.path.join(REPO, 'gradle.properties')):
        if line.startswith('mod_version='):
            return line.split('=', 1)[1].strip()


def java_for(minecraft):
    if minecraft.startswith('26.'):
        return 25
    parts = [int(part) for part in minecraft.split('.')] + [0]
    return 21 if parts[1:3] >= [20, 5] else 17


def latest(metadata_url):
    xml = open(launcher.fetch(metadata_url, os.path.join(RUN, 'installers', urllib.parse.quote(metadata_url, safe='')))).read()
    return re.search(r'<release>([^<]+)</release>', xml).group(1)


def install(loader, minecraft, loader_version, server):
    """Installs the client profile into run/minecraft and a server into its own folder.
    Returns the profile name and the arguments that start the server."""
    java = launcher.java(java_for(minecraft))
    installers = os.path.join(RUN, 'installers')
    os.makedirs(installers, exist_ok=True)
    if not os.path.exists(os.path.join(MINECRAFT, 'launcher_profiles.json')):
        os.makedirs(MINECRAFT, exist_ok=True)
        open(os.path.join(MINECRAFT, 'launcher_profiles.json'), 'w').write('{"profiles":{}}')

    def run(*arguments):
        subprocess.run([java, '-jar'] + list(arguments), cwd=installers, capture_output=True)

    if loader == 'fabric':
        base = 'https://maven.fabricmc.net/net/fabricmc/fabric-installer/'
        release = latest(base + 'maven-metadata.xml')
        installer = launcher.fetch('%s%s/fabric-installer-%s.jar' % (base, release, release), os.path.join(installers, 'fabric.jar'))
        profile = 'fabric-loader-%s-%s' % (loader_version, minecraft)
        client = [installer, 'client', '-dir', MINECRAFT, '-mcversion', minecraft, '-loader', loader_version, '-noprofile']
        run(installer, 'server', '-dir', server, '-mcversion', minecraft, '-loader', loader_version, '-downloadMinecraft')
        start = ['-jar', 'fabric-server-launch.jar', 'nogui']
    elif loader == 'quilt':
        base = 'https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/'
        release = latest(base + 'maven-metadata.xml')
        installer = launcher.fetch('%s%s/quilt-installer-%s.jar' % (base, release, release), os.path.join(installers, 'quilt.jar'))
        profile = 'quilt-loader-%s-%s' % (loader_version, minecraft)
        client = [installer, 'install', 'client', minecraft, loader_version, '--install-dir=' + MINECRAFT, '--no-profile']
        run(installer, 'install', 'server', minecraft, loader_version, '--install-dir=' + server, '--download-server')
        start = ['-jar', 'quilt-server-launch.jar', 'nogui']
    else:
        # NeoForge for 1.20.1 is still a Forge fork and is laid out like Forge
        legacy = loader == 'forge' or minecraft == '1.20.1'
        if loader == 'forge':
            url = 'https://maven.minecraftforge.net/net/minecraftforge/forge/{0}-{1}/forge-{0}-{1}-installer.jar'
        elif legacy:
            url = 'https://maven.neoforged.net/releases/net/neoforged/forge/{0}-{1}/forge-{0}-{1}-installer.jar'
        else:
            url = 'https://maven.neoforged.net/releases/net/neoforged/neoforge/{1}/neoforge-{1}-installer.jar'
        installer = launcher.fetch(url.format(minecraft, loader_version),
                                   os.path.join(installers, '%s-%s-%s.jar' % (loader, minecraft, loader_version)))
        profile = '%s-forge-%s' % (minecraft, loader_version) if legacy else 'neoforge-' + loader_version
        client = [installer, '--installClient' if legacy else '--install-client', MINECRAFT]
        run(installer, '--installServer' if legacy else '--install-server', server)
        arguments = glob.glob(os.path.join(server, 'libraries', 'net', '*', '*', '*', 'unix_args.txt'))
        start = ['@' + os.path.relpath(arguments[0], server), 'nogui'] if arguments else ['-jar', 'server.jar', 'nogui']
    if not os.path.isdir(os.path.join(MINECRAFT, 'versions', profile)):
        run(*client)
    return profile, start


def modrinth(loader, minecraft, slugs):
    """Newest file on Modrinth of each project for this loader and version."""
    files = []
    for slug in slugs:
        query = urllib.parse.urlencode({'loaders': json.dumps(['fabric' if loader == 'quilt' else loader]),
                                        'game_versions': json.dumps([minecraft])})
        listing = launcher.fetch('https://api.modrinth.com/v2/project/%s/version?%s' % (slug, query),
                                 os.path.join(RUN, 'mods', '%s-%s-%s.json' % (slug, loader, minecraft)))
        versions = json.load(open(listing))
        versions = [v for v in versions if v['version_type'] == 'release'] or versions
        if not versions:
            print('  no %s for %s %s, left out' % (slug, loader, minecraft))
            continue
        file = ([f for f in versions[0]['files'] if f['primary']] or versions[0]['files'])[0]
        files.append(launcher.fetch(file['url'], os.path.join(RUN, 'mods', file['filename'])))
    return files


def scene():
    """Console commands that build the test world. The player spawns at 0 -60 0 looking south:
    a sign and two torches on the side of a log and a sign on a log end in front, ladders on
    logs and on stone to the right, a sign with text on a log to the left."""
    commands = [
        # the names of some game rules changed over time, the wrong ones are just rejected
        'gamerule spawnRadius 0', 'gamerule spawn_radius 0', 'gamerule respawn_radius 0',
        'gamerule doDaylightCycle false', 'gamerule advance_time false',
        'gamerule doWeatherCycle false', 'gamerule advance_weather false',
        'gamerule doMobSpawning false', 'gamerule spawn_mobs false',
        'difficulty peaceful', 'kill @e[type=!player]', 'time set noon', 'weather clear',
        'setworldspawn 0 -60 0', 'forceload add -16 -16 16 16',
        'setblock 1 -60 3 minecraft:oak_log[axis=x]',
        'setblock 1 -59 3 minecraft:oak_log',
        'setblock 1 -58 3 minecraft:oak_log',
        'setblock 1 -57 3 minecraft:oak_log',
        'setblock 0 -60 3 minecraft:oak_wall_sign[facing=west]',
        'setblock 0 -59 3 minecraft:oak_wall_sign[facing=west]',
        'setblock 0 -58 3 minecraft:wall_torch[facing=west]',
        'setblock 0 -57 3 minecraft:redstone_wall_torch[facing=west]',
        'setblock -2 -60 3 minecraft:stone',
        'setblock -2 -59 3 minecraft:spruce_log',
        'setblock -2 -58 3 minecraft:spruce_log',
        'setblock -1 -60 3 minecraft:ladder[facing=east]',
        'setblock -1 -59 3 minecraft:ladder[facing=east]',
        'setblock -1 -58 3 minecraft:ladder[facing=east]',
        'setblock 5 -60 6 minecraft:birch_log', 'setblock 5 -59 6 minecraft:birch_log',
        'setblock -5 -60 6 minecraft:stone', 'setblock -5 -59 6 minecraft:stone',
    ]
    # sign text was stored differently before 1.20 and again before 1.21.5, only the right form is accepted
    for x, where in ((5, 'LOG'), (-5, 'STONE')):
        sign = 'setblock %d -59 5 minecraft:oak_wall_sign[facing=north]' % x
        commands += [
            sign + "{Text1:'{\"text\":\"ON\"}',Text2:'{\"text\":\"%s\"}'}" % where,
            sign + "{front_text:{messages:['{\"text\":\"ON\"}','{\"text\":\"%s\"}','{\"text\":\"\"}','{\"text\":\"\"}']}}" % where,
            sign + '{front_text:{messages:["ON","%s","",""]}}' % where,
        ]
    # Keeps the player in place, looking slightly off-axis. With the camera exactly along an
    # axis Forge 1.18 and 1.19 don't draw signs at all, mod or no mod.
    commands.append('setblock 0 -62 0 minecraft:repeating_command_block{Command:"tp @a 0.5 -60.0 0.5 2 2",auto:1b}')
    return commands + ['save-all flush']


def wait_for(log, pattern, process, deadline):
    while time.time() < deadline and process.poll() is None:
        if re.search(pattern, open(log, errors='replace').read()):
            return True
        time.sleep(2)
    return False


def run_server(folder, java, start):
    """Starts the server, builds the scene, stops it again. True if it came up."""
    open(os.path.join(folder, 'eula.txt'), 'w').write('eula=true\n')
    open(os.path.join(folder, 'server.properties'), 'w').write('\n'.join([
        'online-mode=false', 'level-type=flat', 'generate-structures=false', 'gamemode=adventure',
        'spawn-monsters=false', 'spawn-animals=false', 'spawn-npcs=false', 'spawn-protection=0',
        'view-distance=4', 'simulation-distance=4', 'server-port=0', '']))
    log = os.path.join(folder, 'server.log')
    with open(log, 'w') as out:
        server = subprocess.Popen([java, '-Xmx2G'] + start, cwd=folder, stdin=subprocess.PIPE, stdout=out,
                                  stderr=subprocess.STDOUT, text=True)
    up = wait_for(log, r'Done \(', server, time.time() + 400)
    if up:
        for command in scene() + ['stop']:
            server.stdin.write(command + '\n')
            server.stdin.flush()
            time.sleep(0.15)
        try:
            server.wait(90)
        except subprocess.TimeoutExpired:
            pass
    if server.poll() is None:
        server.kill()
    return up


def run_client(profile, folder, quick_play):
    """Runs the client on a virtual display until the player is in the world, takes a
    screenshot with the HUD hidden and stops it. Returns the screenshot, or None."""
    command = launcher.client_command(MINECRAFT, profile, folder, ['-Dmixin.debug.export=true'],
                                      ['--quickPlaySingleplayer', 'test'] if quick_play else [])
    display = ':%d' % (90 + os.getpid() % 100)
    xvfb = subprocess.Popen(['Xvfb', display, '-screen', '0', '854x480x24', '-nolisten', 'tcp'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    env = dict(os.environ, DISPLAY=display, LIBGL_ALWAYS_SOFTWARE='1')
    log = os.path.join(folder, 'client.log')
    with open(log, 'w') as out:
        game = subprocess.Popen(command, cwd=folder, env=env, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    deadline = time.time() + 500
    if not quick_play:
        # No quick play before 1.20. Wait for the title screen, then click
        # Singleplayer, the world and Play Selected World.
        if wait_for(log, r'textures/atlas/blocks\.png-atlas', game, deadline):
            time.sleep(12)
            for x, y in ((427, 236), (427, 136), (269, 396)):
                subprocess.call(['xdotool', 'mousemove', str(x), str(y), 'click', '1'], env=env)
                time.sleep(1.5)
    shot = None
    if wait_for(log, 'Tester joined the game', game, deadline):
        time.sleep(45)
        subprocess.call(['xdotool', 'key', 'F1'], env=env)
        time.sleep(2)
        shot = os.path.join(folder, 'shot.png')
        subprocess.call(['import', '-display', display, '-window', 'root', shot], env=env)
    if game.poll() is None:
        os.killpg(game.pid, signal.SIGTERM)
        try:
            game.wait(20)
        except subprocess.TimeoutExpired:
            os.killpg(game.pid, signal.SIGKILL)
    xvfb.terminate()
    return shot if shot and os.path.exists(shot) else None


def applied_hooks(folder):
    """Names of the mod's mixin handlers in the classes Mixin exported."""
    hooks = set()
    for path in glob.glob(os.path.join(folder, '.mixin.out', 'class', '**', '*.class'), recursive=True):
        hooks.update(name.decode() for name in re.findall(rb'roundtreescompanion\$(\w+)', open(path, 'rb').read()))
    return hooks


def run_case(loader, minecraft, loader_version, jar_name, mods=''):
    name = '%s-%s%s' % (loader, minecraft, '-mods' if mods else '')
    jar = os.path.join(REPO, 'dist', 'RoundTreesCompanion-%s-%s.jar' % (mod_version(), jar_name))
    print('%s (%s%s)' % (name, jar_name, ', with ' + mods if mods else ''))
    if not os.path.exists(jar):
        print('  FAIL: %s is missing, build first' % os.path.relpath(jar, REPO))
        return False

    server = os.path.join(RUN, 'server', name)
    shutil.rmtree(server, ignore_errors=True)
    os.makedirs(os.path.join(server, 'mods'))
    profile, start = install(loader, minecraft, loader_version, server)
    if not os.path.isdir(os.path.join(MINECRAFT, 'versions', profile)):
        print('  FAIL: could not install %s %s for %s' % (loader, loader_version, minecraft))
        return False
    extra = modrinth(loader, minecraft, mods.split(',')) if mods else []

    for file in [jar] + [mod for mod in extra if not CLIENT_ONLY.search(os.path.basename(mod))]:
        shutil.copy(file, os.path.join(server, 'mods'))
    if not run_server(server, launcher.java(java_for(minecraft)), start):
        print('  FAIL: the server did not start, see %s' % os.path.relpath(os.path.join(server, 'server.log'), REPO))
        return False
    print('  server started')

    shots = {}
    for variant in ('with', 'without'):
        client = os.path.join(RUN, 'client', '%s-%s' % (name, variant))
        shutil.rmtree(client, ignore_errors=True)
        os.makedirs(os.path.join(client, 'mods'))
        os.makedirs(os.path.join(client, 'config'))
        shutil.copy(os.path.join(HERE, 'options.txt'), client)
        # NeoForge's loading window can't be created on a virtual display
        open(os.path.join(client, 'config', 'fml.toml'), 'w').write('earlyWindowControl = false\n')
        shutil.copytree(os.path.join(server, 'world'), os.path.join(client, 'saves', 'test'))
        for file in ([jar] if variant == 'with' else []) + extra:
            shutil.copy(file, os.path.join(client, 'mods'))
        shot = run_client(profile, client, quick_play=not minecraft.startswith(('1.18', '1.19')))
        if not shot:
            print('  FAIL: the client %s the mod did not get into the world, see %s'
                  % (variant, os.path.relpath(os.path.join(client, 'client.log'), REPO)))
            return False
        shots[variant] = os.path.join(RUN, 'shots', '%s-%s.png' % (name, variant))
        os.makedirs(os.path.dirname(shots[variant]), exist_ok=True)
        shutil.copy(shot, shots[variant])
        if variant == 'with':
            hooks = applied_hooks(client)
            print('  hooks applied: ' + (', '.join(sorted(hooks)) or 'none'))

    passed = {'getLogOffset', 'shiftSign'} <= hooks
    for label, region in REGIONS.items():
        result = subprocess.run(['compare', '-metric', 'AE', '-fuzz', '12%', '-extract', region,
                                 shots['with'], shots['without'], 'null:'], capture_output=True, text=True)
        changed = int(float((result.stderr.split() or ['0'])[0]))
        print('  %s: %d pixels moved' % (label, changed))
        passed = passed and changed > 0
    print('  PASS' if passed else '  FAIL: compare run/shots/%s-with.png and -without.png' % name)
    return passed


def main():
    if len(sys.argv) > 1:
        cases = [sys.argv[1:]]
    else:
        lines = [line.split('#')[0].split() for line in open(os.path.join(HERE, 'cases.txt'))]
        cases = [line for line in lines if line]
    failed = [' '.join(case) for case in cases if not run_case(*case)]
    print('%d of %d passed' % (len(cases) - len(failed), len(cases)))
    for case in failed:
        print('failed: ' + case)
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
