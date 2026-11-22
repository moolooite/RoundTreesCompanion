package com.roundtrees.roundtreescompanion.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.SignRenderer;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.phys.Vec3;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(SignRenderer.class)
public class SignRendererMixin {

    @Inject(method = "render(Lnet/minecraft/world/level/block/entity/SignBlockEntity;FLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;II)V", at = @At("HEAD"))
    private void roundtreescompanion$shiftSign(SignBlockEntity sign, float partialTick, PoseStack poseStack, MultiBufferSource buffers, int light, int overlay, CallbackInfo ci) {
        Vec3 shift = LogHelper.getShift(sign.getBlockState(), sign.getLevel(), sign.getBlockPos());
        if (shift != Vec3.ZERO) poseStack.translate(shift.x, shift.y, shift.z);
    }
}
