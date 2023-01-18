from custom.LevelSelector import LevelSelector
from custom.MenuScreen import MenuScreen
import lylac;

mainRenderer = lylac.Renderer((1280, 720), 200);

lylac.PreloadService.preloadSprite("assets/ui/direction-arrow.png", (50, 50));

lylac.FontService.loadFont("rubik", "fonts/RubikVinyl.tff");

def MAIN_GAME():
    levelSelector = LevelSelector(mainRenderer);

welcomeScreen = MenuScreen(mainRenderer);

welcomeScreen.onMenuExit.connect(lambda _: MAIN_GAME())

mainRenderer.start(); #always goes at the bottom!

#TODO: make welcome screen c:
#TODO: chess board map
#TODO: make the levels balanced lmfao
#TODO[URGENT]: FIX FONT LOADING