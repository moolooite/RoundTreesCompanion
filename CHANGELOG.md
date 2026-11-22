# Changelog

## 1.2.0

- Added Forge builds for 1.18.2 - 1.20.1
- Added NeoForge builds for 1.21 - 1.21.1 and 26.1 - 26.3
- Added Fabric builds for 1.18.2 - 1.19.4, 1.21.5 - 1.21.11 and 26.1 - 26.3
- The Fabric builds also work on Quilt, and the Forge build on NeoForge 1.20.1
- The 1.21.4 jar now covers 1.21.4 - 1.21.8
- If another mod gets in the way of one of the mod's hooks, that part is now skipped instead of crashing the game
- Fixed a possible crash on 1.21.2+ when a block changed while a chunk with ladders or torches on logs was being rebuilt
- Fabric: now marked as client-only, so dedicated servers skip it
- A little less work per block while chunks are built
- The licence is now included in the jars
- Jars are now named `RoundTreesCompanion-<version>-<loader>-<minecraft>.jar`

## 1.1.0

- Fixed crash on 1.21.x
- Added wall torches, soul torches and redstone torches
- Ladders are now only shifted when placed on logs
- Things on the flat end of sideways logs aren't shifted anymore
- Works with Sodium
- Fabric API is no longer needed
- Separate builds for 1.20 - 1.21.1, 1.21.2 - 1.21.3 and 1.21.4

## 1.0.0

- First release
