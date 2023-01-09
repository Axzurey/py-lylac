import json;
import time;
from typing import TypedDict;

from pygame import Vector2;
from custom.towerWidget import TowerWidget;
from data.Enemy import EnemyManager;
from data.enemies.MidnightEye import MidnightEye
from data.tower import TowerManager;
from data.towers.Marionette import Marionette;
from data.towers.StarBlue import StarBlue;
import lylac;
from lylac.modules.util import createThread;
from custom.LevelSelector import LevelData;

ENEMY_NAMES = {
    "Midnight Eye": MidnightEye
}

class WaveSpawnStatsDiff(TypedDict):
    speedBonus: int | None;
    healthBonus: int | None;

class WaveSpawn(TypedDict):
    enemyName: str;
    enemyDelay: float;
    enemyCount: int;
    enemyStats: WaveSpawnStatsDiff | None;

class Wave(TypedDict):
    prewaveMessage: str | None;
    enemies: list[WaveSpawn];

class LevelController:
    """
    This class is create on a per level basis
    """

    onLevelComplete = lylac.LylacSignal();

    def broadcastMessage(self, msg: str):
        f = lylac.Frame();
        f.size = lylac.Udim2.fromScale(1.2, .15);
        f.anchorPoint = Vector2(.5, .5);
        f.cornerRadius = 0;
        f.position = lylac.Udim2.fromScale(-1, .5);

        t = lylac.TextObject();
        t.anchorPoint = Vector2(.5, .5);
        t.position = lylac.Udim2.fromScale(.5, .5);
        t.size = lylac.Udim2.fromScale(1, 1);
        t.text = msg;
        t.textSize = 40;
        t.textAlignX = "center";
        t.textAlignY = "center";
        t.parent = f;

        f.parent = self.screen;

        lylac.AnimationService.createAnimation(f, "position", lylac.Udim2.fromScale(.5, .5), 1, lylac.InterpolationMode.easeInOutCirc);

        time.sleep(2 + 1);

        lylac.AnimationService.createAnimation(f, "position", lylac.Udim2.fromScale(2, .5), 1, lylac.InterpolationMode.easeInOutCirc);

    def startLevel(self, wavePath: str):
        
        file = open(wavePath, 'r');

        waveData: list[Wave] = json.load(file);

        waveNumber = 0;
        for wave in waveData:
            msg = wave['prewaveMessage'];
            if msg:
                self.broadcastMessage(msg);

            self.towerWidget.show();

            for enemyWave in wave['enemies']:
                
                enemyName = enemyWave['enemyName'];
                enemyStats = enemyWave['enemyStats'] if 'enemyStats' in enemyWave else None;
                enemyCount = enemyWave['enemyCount'];

                for _ in range(enemyCount):
                    time.sleep(enemyWave['enemyDelay']);

                    enemy = ENEMY_NAMES[enemyName](self.backdrop);
                    EnemyManager.addEnemy(enemy);
                    
                    if enemyStats and 'healthBonus' in enemyStats:
                        enemy.health += enemyStats['healthBonus']; #type: ignore it's definitely in there
                    if enemyStats and 'speedBonus' in enemyStats:
                        enemy.speed += enemyStats['speedBonus']; #type: ignore it's definitely in there

            EnemyManager.enemiesEmpty.wait();

            waveNumber += 1;
            self.towerWidget.hide();

        lylac.CleanupService.delay(1, lambda _: self.backdrop.destroy);
        self.onLevelComplete.dispatch(None);

    screen: lylac.Renderer;
    backdrop: lylac.Sprite;
    towerWidget: TowerWidget;

    def __init__(self, screen: lylac.Renderer, levelData: LevelData) -> None:
        self.screen = screen;

        spr = lylac.Sprite();
        spr.parent = screen;
        spr.imagePath = levelData['backdrop'];
        spr.size = lylac.Udim2.fromOffset(1280, 720);
        spr.position = lylac.Udim2();

        self.backdrop = spr;

        entropyIcon = lylac.Sprite();
        entropyIcon.parent = spr;
        entropyIcon.imagePath = "assets/ui/entropy_coin-01.png";
        entropyIcon.size = lylac.Udim2.fromOffset(75, 75);
        entropyIcon.anchorPoint = Vector2(.5, .5);
        entropyIcon.position = lylac.Udim2.fromScale(.9, .05);

        entropyText = lylac.TextObject();
        entropyText.text = "x" + str(TowerManager.playerEntropy);
        entropyText.size = lylac.Udim2.fromScale(.1, .05);
        entropyText.textColor = lylac.Color4.white();
        entropyText.anchorPoint = Vector2(.5, .5);
        entropyText.textAlignX = "center";
        entropyText.textAlignY = "center";
        entropyText.position = lylac.Udim2(75 / 2, .9, 0, .05);
        entropyText.backgroundColor = lylac.Color4.invisible();
        entropyText.borderColor = lylac.Color4.invisible();
        entropyText.dropShadowColor = lylac.Color4.invisible();
        entropyText.parent = spr;

        def setEntropyText(e):
            entropyText.text = "x" + str(e);

        TowerManager.entropyChanged.connect(setEntropyText);

        with open(levelData['path_of_enemies'], 'r') as f:
            path: list[list[float]] = json.loads(f.read());
            
            curve = lylac.SegmentedLineObject(spr);
            curve.color = lylac.Color4(0, 1, 1)
            curve.points = [];
            
            for point in path:
                v = Vector2(point[0], point[1]);
                curve.points.append(v);
            f.close();

            EnemyManager.curve = curve;

        areaPolygons: list[lylac.PolygonObject] = [];

        with open(levelData['area_for_towers'], 'r') as f:
            areas: list[list[list[float]]] = json.loads(f.read());

            for area in areas:
                a = lylac.PolygonObject(spr);
                a.color = lylac.Color4(1, 0, 0);
                a.points = [];
                for point in area:
                    p = Vector2(point[0], point[1]);
                    a.points.append(p);
                areaPolygons.append(a);
            f.close();

        self.towerWidget = TowerWidget(spr, [
            {
                "name": "Star Blue",
                "imagePath": "assets/towers/star-blue.png",
                "cost": 100,
                "radius": 200,
                "link": StarBlue,
                "targetSize": 125,
            },
            {
                "name": "Marionette",
                "imagePath": "assets/towers/marionette-pixel.png",
                "cost": 150,
                "radius": 500,
                "link": Marionette,
                "targetSize": 100,
            }
        ], areaPolygons);

        TowerManager.addEntropy(-1);
        TowerManager.addEntropy(levelData["startingEntropy"]);

        createThread(lambda _: self.startLevel(levelData['wavePath']), None);