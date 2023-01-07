import pygame
import lylac

GAME_LEVELS = {
    "grass patch": {
        "area_for_towers": "levels/grass_patch/towerAreas.json",
        "path_of_enemies": "levels/grass_patch/enemyPath.json",
        "backdrop": "assets/environment/grass patch-01.png",
        "permittedTowers": [
            "Star Blue", "Marionette"
        ]
    }
}

class LevelSelector:

    screen: lylac.Renderer;

    def __init__(self, screen: lylac.Renderer) -> None:
        self.screen = screen;

        display = lylac.Frame();
        display.size = lylac.Udim2.fromScale(1, 1);
        display.parent = screen;
        display.backgroundColor = lylac.Color4.fromRGB(25, 25, 50);