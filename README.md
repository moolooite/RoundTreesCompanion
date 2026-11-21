# Round Trees Companion

A Minecraft Fabric mod that prevents z-fighting between wall signs, ladders, torches, and round tree texture packs by subtly shifting them forward when placed on logs.

## Features

- **Wall Sign Compatibility**: Automatically shifts wall signs forward by 1/16 block when placed on any log block
- **Ladder Compatibility**: Shifts ladders forward when placed on logs to prevent visual clipping with round tree textures
- **Torch Compatibility**: Shifts wall torches, soul torches and redstone torches forward when placed on logs
- **Seamless Integration**: Works automatically without configuration - just install and play
- **Texture Pack Agnostic**: Compatible with any round tree texture pack

## Compatibility

- **Minecraft**: 1.20.0 - 1.21.4
- **Mod Loader**: Fabric Loader 0.14.0+
- **Dependencies**: None

There are separate downloads for 1.20 - 1.21.1, 1.21.2 - 1.21.3 and 1.21.4, make sure to grab the one for your version.

## Installation

1. Install [Fabric Loader](https://fabricmc.net/use/installer/) for your Minecraft version
2. Download Round Trees Companion from [Modrinth](https://modrinth.com/mod/round-trees-companion) and place it in your mods folder
3. Launch Minecraft with the Fabric profile

## How It Works

### Wall Signs
The mod uses a client-side mixin to detect when wall signs are placed on log blocks and automatically translates their rendering position forward by 1/16 block (1 pixel). This prevents the sign from appearing to "sink into" round tree textures.

### Ladders and Torches
Ladders and wall torches placed on logs are moved forward using the block's model offset (the same thing vanilla uses to randomly offset flowers). Ladders are shifted by 1.4 pixels and torches by 1 pixel. Ladders and torches on other blocks aren't touched.

Signs, ladders and torches on the flat end of a sideways log are left alone, since round tree packs don't change log ends.

## Technical Details

- **Wall Signs**: Implemented via `SignBlockEntityRendererMixin` that checks for log blocks behind wall signs
- **Ladders and Torches**: Implemented via `BlockStateMixin` which offsets the model of ladders and wall torches on logs, this also works with Sodium
- **Performance**: Minimal performance impact - only processes wall signs, ladders and wall torches

## Supported Blocks

### Logs (Auto-detected via BlockTags.LOGS)
- Oak Log
- Spruce Log  
- Birch Log
- Jungle Log
- Acacia Log
- Dark Oak Log
- Mangrove Log
- Cherry Log
- Crimson Stem
- Warped Stem
- And any modded logs that use the `#minecraft:logs` tag

### Signs
- All vanilla wall sign variants (oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, bamboo, crimson, warped)
- Compatible with modded wall signs that extend `WallSignBlock`

### Torches
- Wall torches, soul torches and redstone torches
- Compatible with modded wall torches that extend `WallTorchBlock`

## FAQ

**Q: Will this affect signs, ladders or torches placed on other blocks?**  
A: No, the mod only shifts them when they're placed specifically on log blocks.

**Q: Is this compatible with other sign mods?**  
A: Yes, as long as they extend the vanilla `WallSignBlock` class.

**Q: Does this work with Sodium?**  
A: Yes.

**Q: Does this work in multiplayer?**  
A: Yes, this is a client-side only mod that works on any server.

**Q: Will this break my existing signs?**  
A: No, existing signs will automatically benefit from the fix without any changes needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Issues & Support

Found a bug or have a suggestion? Please open an issue on the [GitHub repository](https://github.com/moolooite/RoundTreesCompanion).
