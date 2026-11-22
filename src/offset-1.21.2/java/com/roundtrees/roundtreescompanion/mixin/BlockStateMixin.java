package com.roundtrees.roundtreescompanion.mixin;

import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

// Block models are shifted through the model offset so it also works with Sodium
@Mixin(BlockBehaviour.BlockStateBase.class)
public abstract class BlockStateMixin {

    @Shadow
    public abstract Block getBlock();

    @Shadow
    protected abstract BlockState asState();

    // If the shape cache patch is missing vanilla would throw for ladders, so nothing is reported then
    @Inject(method = "hasOffsetFunction", at = @At("HEAD"), cancellable = true)
    private void roundtreescompanion$hasLogOffset(CallbackInfoReturnable<Boolean> cir) {
        if (LogHelper.isShiftedModel(getBlock()) && LogHelper.shapeCachePatched) cir.setReturnValue(true);
    }

    @Inject(method = "getOffset", at = @At("HEAD"), cancellable = true)
    private void roundtreescompanion$getLogOffset(BlockPos pos, CallbackInfoReturnable<Vec3> cir) {
        if (!LogHelper.isShiftedModel(getBlock())) return;

        Vec3 shift = Vec3.ZERO;
        try {
            shift = LogHelper.getShift(asState(), Minecraft.getInstance().level, pos);
        } catch (RuntimeException e) {
            // Chunks are built off-thread and the level can change under the lookup, skip the shift this once
        }
        cir.setReturnValue(shift);
    }
}
