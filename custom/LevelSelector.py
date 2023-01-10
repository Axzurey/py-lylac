from typing import TypedDict
import pygame
from data.tower import TowerManager
import lylac

class LevelData(TypedDict):
    area_for_towers: str;
    path_of_enemies: str;
    backdrop: str;
    permittedTowers: list[str];
    wavePath: str;
    startingEntropy: int;

GAME_LEVELS: dict[str, LevelData] = {
    "grass patch": {
        "area_for_towers": "levels/grass_patch/towerAreas.json",
        "path_of_enemies": "levels/grass_patch/enemyPath.json",
        "backdrop": "assets/environment/grass patch-01.png",
        "wavePath": "levels/grass_patch/waveData.json",
        "permittedTowers": [
            "Star Blue", "Marionette", "Particle Collider"
        ],
        "startingEntropy": 150
    },
    "grass patch II": {
        "area_for_towers": "levels/grass_patch_2/towerAreas.json",
        "path_of_enemies": "levels/grass_patch_2/enemyPath.json",
        "backdrop": "assets/environment/grass patch 2-01.png",
        "wavePath": "levels/grass_patch_2/waveData.json",
        "permittedTowers": [
            "Star Blue", "Marionette", "Particle Collider"
        ],
        "startingEntropy": 200
    },
}

def boxLayout(index: int, grid: pygame.Vector2, size: pygame.Vector2, padding: pygame.Vector2):
    xIndex = index % grid.x;
    yIndex = index // (grid.y + 1);

    return pygame.Vector2(size.x * xIndex + padding.x * xIndex, size.y * yIndex + padding.y * yIndex);

class LevelSelector:

    screen: lylac.Renderer;
    display: lylac.Frame | None = None;

    def spawnLevel(self, level: str):
        self.hide();
        TowerManager.playerEntropy = 0;

        from custom.LevelController import LevelController

        levelController = LevelController(self.screen, GAME_LEVELS[level]);
        levelController.onLevelComplete.connect(lambda _: self.show());

    def __init__(self, screen: lylac.Renderer) -> None:
        self.screen = screen;

        self.show();

    def hide(self):
        self.display.destroy() if self.display else ...;

    def show(self):
        display = lylac.Frame();
        display.size = lylac.Udim2.fromScale(1, 1);
        display.parent = self.screen;
        display.backgroundColor = lylac.Color4.fromRGB(25, 25, 50);
        display.position = lylac.Udim2();
        display.cornerRadius = 0;

        self.display = display;

        levelIndex = 0;

        for level in GAME_LEVELS:
            def fuck_python():

                levelName = level;

                levelData = GAME_LEVELS[level];
                calculatedPosition = boxLayout(levelIndex, pygame.Vector2(3, 2), pygame.Vector2(300, 150), pygame.Vector2(50, 50));
                
                levelDisplayBackdrop = lylac.Frame();
                levelDisplayBackdrop.position = lylac.Udim2(calculatedPosition.x, .2, calculatedPosition.y, .2);
                levelDisplayBackdrop.size = lylac.Udim2.fromOffset(300, 150);
                levelDisplayBackdrop.anchorPoint = pygame.Vector2(.5, .5);
                levelDisplayBackdrop.parent = display;
                levelDisplayBackdrop.borderColor = lylac.Color4(0, 1, 0)
                levelDisplayBackdrop.backgroundColor = lylac.Color4(0, 1, 0);
                levelDisplayBackdrop.name = "display-backdrop";
                
                levelDisplay = lylac.Sprite();
                levelDisplay.size = lylac.Udim2.fromScale(.95, .95);
                levelDisplay.position = lylac.Udim2.fromScale(.5, .5);
                levelDisplay.anchorPoint = pygame.Vector2(.5, .5);
                levelDisplay.imagePath = levelData['backdrop'];
                levelDisplay.parent = levelDisplayBackdrop;

                levelText = lylac.TextButton();
                levelText.size = lylac.Udim2.fromScale(1, 1);
                levelText.position = lylac.Udim2.fromScale(.5, .5);
                levelText.anchorPoint = pygame.Vector2(.5, .5);
                levelText.text = level;
                levelText.parent = levelDisplay;
                levelText.backgroundColor = lylac.Color4.fromAlpha(0);
                levelText.borderColor = lylac.Color4.fromAlpha(0);
                levelText.dropShadowColor = lylac.Color4.fromAlpha(0);
                levelText.textAlignX = "center";
                levelText.textAlignY = "center";
                levelText.textSize = 24;
                levelText.textColor = lylac.Color4()

                styleConnection = lylac.useActionState(
                    levelText,
                    defaultProperties={"size": lylac.Udim2.fromOffset(300, 150)},
                    hoverProperties={"size": lylac.Udim2.fromOffset(320, 170)},
                    forInstance=levelDisplayBackdrop
                )

                styleConnection2 = lylac.useActionState(
                    levelText,
                    defaultProperties={"textSize": 24},
                    hoverProperties={"textSize": 27},
                )

                levelText.onMouseButton1Up.connect(lambda _: self.spawnLevel(levelName))

            fuck_python();

            levelIndex += 1;