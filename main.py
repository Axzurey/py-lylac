from custom.LevelSelector import LevelSelector
import lylac;

mainRenderer = lylac.Renderer((1280, 720), 200);

lylac.PreloadService.preloadSprite("assets/ui/direction-arrow.png", (50, 50))

levelSelector = LevelSelector(mainRenderer);

mainRenderer.start(); #always goes at the bottom!

#TODO: add entropy gain on kill