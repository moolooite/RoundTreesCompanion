# Round Trees Companion

Round tree resource packs make logs round, so anything hung on the side of a log ends up clipping into the bark. This mod nudges wall signs, ladders and wall torches forward a little when they're placed on a log.

- Wall signs: 1 pixel
- Ladders: 1.4 pixels
- Wall torches, soul wall torches and redstone wall torches: 1 pixel

Only blocks on the side of a log are moved. On other blocks, and on the flat end of a sideways log, nothing changes. Logs are anything in the `#minecraft:logs` tag, so modded logs work if they're tagged.

The shift is visual only. Hitboxes, placement and the world itself are untouched.

## Downloads

| Loader | Minecraft | File |
| --- | --- | --- |
| Fabric, Quilt, NeoForge | 26.1 - 26.3 | `fabric-neoforge-26.1-26.3` |
| Fabric, Quilt | 1.21.9 - 1.21.11 | `fabric-1.21.9-1.21.11` |
| Fabric, Quilt | 1.21.4 - 1.21.8 | `fabric-1.21.4-1.21.8` |
| Fabric, Quilt | 1.21.2 - 1.21.3 | `fabric-1.21.2-1.21.3` |
| Fabric, Quilt | 1.18.2 - 1.21.1 | `fabric-1.18.2-1.21.1` |
| NeoForge | 1.21 - 1.21.1 | `neoforge-1.21-1.21.1` |
| Forge | 1.18.2 - 1.20.1 | `forge-1.18.2-1.20.1` |

The Forge file also works on NeoForge 1.20.1.

Get them from [Modrinth](https://modrinth.com/mod/roundtreescompanion) or [CurseForge](https://www.curseforge.com/minecraft/mc-mods/roundtreescompanion).

## Requirements

- No dependencies. Fabric API is not needed.
- Client only. Servers don't need it and it works on any server. If it ends up in a server's mods folder it does nothing there.
- A round tree resource pack, such as [Round Trees](https://modrinth.com/resourcepack/round-trees). Without one the mod still works, there's just nothing to fix.

## Install

1. Install Fabric, Quilt, NeoForge or Forge for your Minecraft version.
2. Put the jar for your loader and version in the `mods` folder.

## Compatibility

Works with Sodium, Embeddium and Iris. It adds no blocks, items, config or network traffic, and it only does anything while a wall sign, ladder or wall torch is being drawn, so it's safe to drop into any pack. If another mod gets in the way of one of its hooks, that part is skipped instead of crashing.

One known limit on 1.21.2 and newer: ladders, torches and signs drawn from a world you're not in (schematic previews, moving contraptions) may not be shifted correctly.

## Building

Needs JDK 25 to run Gradle. JDK 17 and 21 are also used and get downloaded if missing.

```bash
./gradlew build
```

All jars end up in `dist/`. Each folder in `versions/` is one jar, its `gradle.properties` says which Minecraft version it's built against and which folders in `src/` it uses.

## Testing

```bash
tests/launchtest.py
```

Launches every jar in `dist/` on a real client and server, see [docs/maintaining.md](docs/maintaining.md).

## Links

- [Modrinth](https://modrinth.com/mod/roundtreescompanion)
- [CurseForge](https://www.curseforge.com/minecraft/mc-mods/roundtreescompanion)
- [GitHub](https://github.com/moolooite/RoundTreesCompanion)

## License

[MIT](LICENSE)
