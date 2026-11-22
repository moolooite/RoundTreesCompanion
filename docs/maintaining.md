# Maintaining

Listing text and upload settings for GitHub, Modrinth and CurseForge. Release notes are taken from [`CHANGELOG.md`](../CHANGELOG.md).

## Summary

[`summary.md`](summary.md), shared by the GitHub About line and the summary field on Modrinth and CurseForge.

## Topics and tags

[`topics.md`](topics.md), the GitHub topics and the categories on Modrinth and CurseForge.

## Description

[`description.md`](description.md), shared by Modrinth and CurseForge.

## Upload settings

Environment is client on both sites. `<version>` is `mod_version` in `gradle.properties`.

| File | Loaders | Game versions |
| --- | --- | --- |
| `RoundTreesCompanion-<version>-fabric-neoforge-26.1-26.3.jar` | Fabric, Quilt, NeoForge | 26.1, 26.1.1, 26.1.2, 26.2, 26.3 |
| `RoundTreesCompanion-<version>-fabric-1.21.9-1.21.11.jar` | Fabric, Quilt | 1.21.9, 1.21.10, 1.21.11 |
| `RoundTreesCompanion-<version>-fabric-1.21.4-1.21.8.jar` | Fabric, Quilt | 1.21.4, 1.21.5, 1.21.6, 1.21.7, 1.21.8 |
| `RoundTreesCompanion-<version>-fabric-1.21.2-1.21.3.jar` | Fabric, Quilt | 1.21.2, 1.21.3 |
| `RoundTreesCompanion-<version>-fabric-1.18.2-1.21.1.jar` | Fabric, Quilt | 1.18.2, 1.19, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.20, 1.20.1, 1.20.2, 1.20.3, 1.20.4, 1.20.5, 1.20.6, 1.21, 1.21.1 |
| `RoundTreesCompanion-<version>-neoforge-1.21-1.21.1.jar` | NeoForge | 1.21, 1.21.1 |
| `RoundTreesCompanion-<version>-forge-1.18.2-1.20.1.jar` | Forge, NeoForge | 1.18.2, 1.19, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.20, 1.20.1 |

NeoForge on the last file is for 1.20.1 only, NeoForge doesn't exist for anything older.

Modrinth version numbers are unique per file: the file name without `RoundTreesCompanion-` and `.jar`, for example `1.2.0-fabric-1.18.2-1.21.1`.
