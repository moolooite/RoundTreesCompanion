package com.roundtrees.roundtreescompanion.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.client.model.Model;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.AbstractSignRenderer;
import net.minecraft.world.level.block.SignBlock;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.WoodType;
import net.minecraft.world.phys.Vec3;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

// render() gained a parameter in 1.21.5, this is the first thing it calls and stayed the same
@Mixin(AbstractSignRenderer.class)
public class SignRendererMixin {

    @Inject(method = "renderSignWithText", at = @At("HEAD"))
    private void roundtreescompanion$shiftSign(SignBlockEntity sign, PoseStack poseStack, MultiBufferSource buffers, int light, int overlay, BlockState state, SignBlock block, WoodType type, Model model, CallbackInfo ci) {
        Vec3 shift = LogHelper.getShift(state, sign.getLevel(), sign.getBlockPos());
        if (shift != Vec3.ZERO) poseStack.translate(shift.x, shift.y, shift.z);
    }
}
