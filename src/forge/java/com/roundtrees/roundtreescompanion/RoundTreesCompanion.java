package com.roundtrees.roundtreescompanion;

import net.minecraftforge.fml.IExtensionPoint;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.network.NetworkConstants;

@Mod("roundtreescompanion")
public class RoundTreesCompanion {

    @SuppressWarnings("removal")
    public RoundTreesCompanion() {
        // Client-only, so servers without the mod aren't shown as incompatible
        ModLoadingContext.get().registerExtensionPoint(IExtensionPoint.DisplayTest.class,
                () -> new IExtensionPoint.DisplayTest(() -> NetworkConstants.IGNORESERVERONLY, (version, fromServer) -> true));
    }
}
