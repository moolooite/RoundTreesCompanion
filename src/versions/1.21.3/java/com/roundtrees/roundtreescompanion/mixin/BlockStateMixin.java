package com.roundtrees.roundtreescompanion.mixin;

import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.BlockState;
import net.minecraft.client.MinecraftClient;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Vec3d;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

// Ladders and wall torches are shifted through the model offset so it also works with Sodium
@Mixin(AbstractBlock.AbstractBlockState.class)
public abstract class BlockStateMixin {

    @Shadow
    protected abstract BlockState asBlockState();

    @Inject(method = "hasModelOffset", at = @At("HEAD"), cancellable = true)
    private void hasLogOffset(CallbackInfoReturnable<Boolean> cir) {
        if (LogHelper.isShiftedModel(asBlockState().getBlock())) cir.setReturnValue(true);
    }

    @Inject(method = "getModelOffset", at = @At("HEAD"), cancellable = true)
    private void getLogOffset(BlockPos pos, CallbackInfoReturnable<Vec3d> cir) {
        BlockState state = asBlockState();
        if (LogHelper.isShiftedModel(state.getBlock())) cir.setReturnValue(LogHelper.getShift(state, MinecraftClient.getInstance().world, pos));
    }
}
