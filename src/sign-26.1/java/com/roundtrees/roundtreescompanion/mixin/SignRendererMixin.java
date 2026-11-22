package com.roundtrees.roundtreescompanion.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import com.roundtrees.roundtreescompanion.LogHelper;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.blockentity.AbstractSignRenderer;
import net.minecraft.client.renderer.blockentity.state.SignRenderState;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

// On 26.1 this draws the whole sign, from 26.2 only the text
@Mixin(AbstractSignRenderer.class)
public class SignRendererMixin {

    @Inject(method = "submit(Lnet/minecraft/client/renderer/blockentity/state/SignRenderState;Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/SubmitNodeCollector;Lnet/minecraft/client/renderer/state/level/CameraRenderState;)V", at = @At("HEAD"))
    private void roundtreescompanion$shiftSign(SignRenderState state, PoseStack poseStack, SubmitNodeCollector collector, CameraRenderState camera, CallbackInfo ci) {
        BlockState blockState = ((BlockEntityRenderStateAccessor) state).roundtreescompanion$getBlockState();
        if (blockState == null) return;

        Vec3 shift = LogHelper.getShift(blockState, Minecraft.getInstance().level, state.blockPos);
        if (shift != Vec3.ZERO) poseStack.translate(shift.x, shift.y, shift.z);
    }
}
