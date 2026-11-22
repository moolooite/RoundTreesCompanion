package com.roundtrees.roundtreescompanion.mixin;

import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.world.level.block.state.BlockState;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

// Vanilla doesn't allow a model offset on blocks with a collision shape, the offset here is only visual
@Mixin(targets = "net.minecraft.world.level.block.state.BlockBehaviour$BlockStateBase$Cache")
public class ShapeCacheMixin {

    @Redirect(method = "<init>", at = @At(value = "INVOKE", target = "Lnet/minecraft/world/level/block/state/BlockState;hasOffsetFunction()Z"), require = 0, expect = 0)
    private boolean roundtreescompanion$ignoreShiftedModels(BlockState state) {
        if (!LogHelper.shapeCachePatched) LogHelper.shapeCachePatched = true;
        return !LogHelper.isShiftedModel(state.getBlock()) && state.hasOffsetFunction();
    }
}
