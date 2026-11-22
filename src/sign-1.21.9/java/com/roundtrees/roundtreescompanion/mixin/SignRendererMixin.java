package com.roundtrees.roundtreescompanion.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.blockentity.AbstractSignRenderer;
import net.minecraft.client.renderer.blockentity.state.SignRenderState;
import net.minecraft.client.renderer.state.CameraRenderState;
import net.minecraft.world.phys.Vec3;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(AbstractSignRenderer.class)
public class SignRendererMixin {

    @Inject(method = "submit(Lnet/minecraft/client/renderer/blockentity/state/SignRenderState;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/SubmitNodeCollector;Lnet/minecraft/client/renderer/state/CameraRenderState;)V", at = @At("HEAD"))
    private void roundtreescompanion$shiftSign(SignRenderState state, PoseStack poseStack, SubmitNodeCollector collector, CameraRenderState camera, CallbackInfo ci) {
        Vec3 shift = LogHelper.getShift(state.blockState, Minecraft.getInstance().level, state.blockPos);
        if (shift != Vec3.ZERO) poseStack.translate(shift.x, shift.y, shift.z);
    }
}
