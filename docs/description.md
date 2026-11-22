Round tree resource packs make logs round, which looks great until you hang something on one: signs, ladders and torches end up clipping into the bark. **Round Trees Companion** fixes that by nudging them forward slightly, but only when they're on a log.

Made by **Astrophyllite**.

## What it does

- **Wall signs** on a log are moved forward by 1 pixel
- **Ladders** on a log are moved forward by 1.4 pixels
- **Wall torches**, soul wall torches and redstone wall torches on a log are moved forward by 1 pixel
- Anything on another block, or on the flat end of a sideways log, is left alone

It works with vanilla logs and stems and with any modded log in the `#minecraft:logs` tag. The change is visual only: hitboxes, placement and your world are untouched, and you can add or remove the mod at any time.

## Which file do I need?

- **Fabric, Quilt or NeoForge, 26.1 - 26.3**: `fabric-neoforge-26.1-26.3`
- **Fabric or Quilt, 1.21.9 - 1.21.11**: `fabric-1.21.9-1.21.11`
- **Fabric or Quilt, 1.21.4 - 1.21.8**: `fabric-1.21.4-1.21.8`
- **Fabric or Quilt, 1.21.2 - 1.21.3**: `fabric-1.21.2-1.21.3`
- **Fabric or Quilt, 1.18.2 - 1.21.1**: `fabric-1.18.2-1.21.1`
- **NeoForge, 1.21 - 1.21.1**: `neoforge-1.21-1.21.1`
- **Forge, 1.18.2 - 1.20.1**: `forge-1.18.2-1.20.1` (also works on NeoForge 1.20.1)

## For modpacks

It's built to be dropped into any pack and forgotten:

- **Client only.** Servers don't need it and it works on any server. If it ends up on a server anyway, it does nothing there.
- **No dependencies.** No Fabric API, no libraries, no config file.
- **Tiny.** Under 10 KB. It adds no blocks, items, packets or data, so it can't affect worlds or saves.
- **Next to nothing at runtime.** No tick or frame handlers. It only does work while a wall sign, ladder or wall torch is being drawn.
- **Plays nicely with others.** Works with Sodium, Embeddium and Iris. If another mod gets in the way of one of its hooks, that part is skipped instead of crashing.

You don't need a specific resource pack, it works with any pack that makes logs round.

One known limit on 1.21.2 and newer: ladders, torches and signs drawn from a world you're not in (schematic previews, moving contraptions) may not be shifted correctly.

## Links

- [Modrinth](https://modrinth.com/mod/roundtreescompanion)
- [CurseForge](https://www.curseforge.com/minecraft/mc-mods/roundtreescompanion)
- [GitHub](https://github.com/moolooite/RoundTreesCompanion) for source and bug reports

MIT licensed. Use it in any modpack, no need to ask.
