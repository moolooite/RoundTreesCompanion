package com.roundtrees.roundtreescompanion.mixin;

import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.block.BlockState;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

// Vanilla doesn't allow a model offset on blocks with a collision shape, the offset here is only visual
@Mixin(targets = "net.minecraft.block.AbstractBlock$AbstractBlockState$ShapeCache")
public class ShapeCacheMixin {

    @Redirect(method = "<init>", at = @At(value = "INVOKE", target = "Lnet/minecraft/block/BlockState;hasModelOffset()Z"))
    private boolean ignoreShiftedModels(BlockState state) {
        return !LogHelper.isShiftedModel(state.getBlock()) && state.hasModelOffset();
    }
}
