package com.roundtrees.roundtreescompanion;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.LadderBlock;
import net.minecraft.block.WallRedstoneTorchBlock;
import net.minecraft.block.WallSignBlock;
import net.minecraft.block.WallTorchBlock;
import net.minecraft.registry.tag.BlockTags;
import net.minecraft.state.property.Properties;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.BlockView;

public class LogHelper {
    public static final double SIGN_SHIFT = 0.0625;
    public static final double LADDER_SHIFT = 0.0875;
    public static final double TORCH_SHIFT = 0.0625;

    // Ladders and wall torches are moved with the block model offset
    public static boolean isShiftedModel(Block block) {
        return block instanceof LadderBlock || block instanceof WallTorchBlock || block instanceof WallRedstoneTorchBlock;
    }

    public static Vec3d getShift(BlockState state, BlockView world, BlockPos pos) {
        if (world == null || !state.contains(Properties.HORIZONTAL_FACING)) return Vec3d.ZERO;

        Block block = state.getBlock();
        double amount;
        if (block instanceof WallSignBlock) {
            amount = SIGN_SHIFT;
        } else if (block instanceof LadderBlock) {
            amount = LADDER_SHIFT;
        } else if (isShiftedModel(block)) {
            amount = TORCH_SHIFT;
        } else {
            return Vec3d.ZERO;
        }

        Direction facing = state.get(Properties.HORIZONTAL_FACING);
        BlockState backState = world.getBlockState(pos.offset(facing.getOpposite()));
        if (!backState.isIn(BlockTags.LOGS)) return Vec3d.ZERO;

        // Sideways logs pointing at the block show their flat end, which round tree packs don't change
        if (backState.contains(Properties.AXIS) && backState.get(Properties.AXIS) == facing.getAxis()) return Vec3d.ZERO;

        return Vec3d.of(facing.getVector()).multiply(amount);
    }
}
