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

mainRenderer = lylac.Renderer((1280, 720), 200);

lylac.PreloadService.preloadSprite("assets/ui/direction-arrow.png", (50, 50));

lylac.FontService.loadFont("rubik", "./fonts/RubikVinyl.ttf");

def MAIN_GAME():
    levelSelector = LevelSelector(mainRenderer);

welcomeScreen = MenuScreen(mainRenderer);

welcomeScreen.onMenuExit.connect(lambda _: MAIN_GAME());

mainRenderer.start(); #always goes at the bottom!

#TODO: chess board map
#TODO: make the levels balanced lmfao
#TODO: projectiles buggin, fix em