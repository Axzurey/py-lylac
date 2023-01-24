"""
This code was made by michael c:
c:
c:
c:

Culminating assignment for ICS year 2022-2023
"""

from custom.LevelSelector import LevelSelector
from custom.MenuScreen import MenuScreen
import lylac;

mainRenderer = lylac.Renderer("Bloom TD [@lylac.fpsfps]", (1280, 720), 200, "assets/ui/entropy_coin-01.png");

lylac.PreloadService.preloadSprite("assets/ui/direction-arrow.png", (50, 50));

lylac.FontService.loadFont("rubik", "./fonts/RubikVinyl.ttf");
lylac.FontService.loadFont("rubikPaint", "./fonts/RubikPaint.ttf");

def MAIN_GAME():
    levelSelector = LevelSelector(mainRenderer);

welcomeScreen = MenuScreen(mainRenderer);

welcomeScreen.onMenuExit.connect(lambda _: MAIN_GAME());

mainRenderer.start(); #always goes at the bottom!