package com.roundtrees.roundtreescompanion;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.LadderBlock;
import net.minecraft.world.level.block.RedstoneWallTorchBlock;
import net.minecraft.world.level.block.WallSignBlock;
import net.minecraft.world.level.block.WallTorchBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.phys.Vec3;

public final class LogHelper {
    private static final double SIGN_SHIFT = 0.0625;
    private static final double LADDER_SHIFT = 0.0875;
    private static final double TORCH_SHIFT = 0.0625;

    // Set by ShapeCacheMixin once its patch is known to be in place
    public static volatile boolean shapeCachePatched;

    // Ladders and wall torches are moved with the block model offset.
    // Wall signs too, since 26.2 their board is a block model and only the text is left to the sign renderer
    public static boolean isShiftedModel(Block block) {
        return block instanceof LadderBlock || block instanceof WallTorchBlock || block instanceof RedstoneWallTorchBlock || block instanceof WallSignBlock;
    }

    public static Vec3 getShift(BlockState state, BlockGetter level, BlockPos pos) {
        Block block = state.getBlock();
        double amount;
        if (block instanceof WallSignBlock) {
            amount = SIGN_SHIFT;
        } else if (block instanceof LadderBlock) {
            amount = LADDER_SHIFT;
        } else if (block instanceof WallTorchBlock || block instanceof RedstoneWallTorchBlock) {
            amount = TORCH_SHIFT;
        } else {
            return Vec3.ZERO;
        }

        if (level == null || !state.hasProperty(BlockStateProperties.HORIZONTAL_FACING)) return Vec3.ZERO;

        Direction facing = state.getValue(BlockStateProperties.HORIZONTAL_FACING);
        BlockState backState = level.getBlockState(pos.relative(facing, -1));
        if (!backState.is(BlockTags.LOGS)) return Vec3.ZERO;

        // Sideways logs pointing at the block show their flat end, which round tree packs don't change
        if (backState.hasProperty(BlockStateProperties.AXIS) && backState.getValue(BlockStateProperties.AXIS) == facing.getAxis()) return Vec3.ZERO;

        return new Vec3(facing.getStepX() * amount, 0, facing.getStepZ() * amount);
    }
}
