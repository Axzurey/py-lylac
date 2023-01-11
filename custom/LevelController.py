import json
import math;
import time;
from typing import Any, TypedDict;

from pygame import Vector2;
from custom.towerWidget import TowerWidget;
from data.Enemy import EnemyManager;
from data.enemies.MidnightEye import MidnightEye
from data.tower import TowerManager;
from data.towers.Marionette import Marionette
from data.towers.ParticleCollider import ParticleCollider;
from data.towers.StarBlue import StarBlue;
import lylac;
from lylac.modules.util import createThread;
from custom.LevelSelector import LevelData
from lylac.services.RenderService import RenderService;

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

        TowerManager.healthChanged.connect(lambda n: (self.backdrop.destroy(), self.onLevelComplete.dispatch(None)) if n <= 0 else...);

        waveNumber = 0;
        for wave in waveData:
            if not self.backdrop.parent: return;
            msg = wave['prewaveMessage'];
            if msg:
                self.broadcastMessage(msg);

            self.towerWidget.show();

            for enemyWave in wave['enemies']:

                if not self.backdrop.parent: return;
                
                enemyName = enemyWave['enemyName'];
                enemyStats = enemyWave['enemyStats'] if 'enemyStats' in enemyWave else None;
                enemyCount = enemyWave['enemyCount'];

                for _ in range(enemyCount):
                    if not self.backdrop.parent: return;
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

        lylac.CleanupService.delay(1, lambda _: self.backdrop.destroy, None);
        self.onLevelComplete.dispatch(None);

    def displayLevelPath(self):
        poverty = False;
        
        insts: list[dict[str, Any]] = [];
        for i in range(3):
            inst = lylac.Sprite();
            inst.imagePath = "assets/ui/direction-arrow.png";
            inst.name = "level-path-guide";
            inst.size = lylac.Udim2.fromOffset(50, 50);
            inst.anchorPoint = Vector2(.5, .5);
            inst.parent = self.backdrop;
            insts.append({"t": i * .02, "inst": inst});

        def displayDelta(dt: float):
            nonlocal c0;
            
            for n, bin in enumerate(insts):
                t = bin["t"];
                t = lylac.clamp(0, 1, t + dt / 2);
                bin["t"] = t;

                inst = bin["inst"];

                if t >= 1:
                    inst.destroy();
                    if n == 0:
                        nonlocal poverty;
                        poverty = True;
                else:
                    nextT = lylac.clamp(0, 1, t + dt / 2);

                    p0 = EnemyManager.curve.getDeltaAlongLine(t);
                    p1 = EnemyManager.curve.getDeltaAlongLine(nextT);

                    if not p0 or not p1: continue;

                    dir = (p1 - p0).normalize();

                    rotation = (int(math.degrees(math.atan2(dir.y, dir.x))) + 90) % 360;

                    inst.position = lylac.Udim2.fromOffset(p0.x, p0.y);
                    inst.rotation = rotation;


        c0 = lylac.RenderService.postRender.connect(displayDelta);

        while not poverty:
            time.sleep(1 / RenderService.renderer.framerate);
        c0.disconnect();
        time.sleep(.25);

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
        entropyText.textAlignX = "left";
        entropyText.textAlignY = "center";
        entropyText.position = lylac.Udim2(100, .9, 0, .05);
        entropyText.backgroundColor = lylac.Color4.invisible();
        entropyText.borderColor = lylac.Color4.invisible();
        entropyText.dropShadowColor = lylac.Color4.invisible();
        entropyText.parent = spr;

        def setEntropyText(e):
            entropyText.text = "x" + str(e);

        TowerManager.entropyChanged.connect(setEntropyText);

        healthIcon = lylac.Sprite();
        healthIcon.imagePath = "assets/ui/heart-icon.png";
        healthIcon.size = lylac.Udim2.fromOffset(65, 65);
        healthIcon.anchorPoint = Vector2(.5, .5);
        healthIcon.position = lylac.Udim2.fromScale(.82, .05);
        healthIcon.parent = spr;

        healthText = lylac.TextObject();
        healthText.textAlignX = "left";
        healthText.textAlignY = "center";
        healthText.anchorPoint = Vector2(.5, .5);
        healthText.textColor = lylac.Color4.white();
        healthText.backgroundColor = lylac.Color4.invisible();
        healthText.borderColor = lylac.Color4.invisible();
        healthText.dropShadowColor = lylac.Color4.invisible();
        healthText.text = "x" + str(TowerManager.playerHealth);
        healthText.position = lylac.Udim2(110, .82, 0, .05);
        healthText.parent = spr;

        def setHealthText(e):
            healthText.text = "x" + str(e);

        TowerManager.healthChanged.connect(setHealthText);

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
            },
            {
                "name": "Particle Collider",
                "imagePath": "assets/towers/particle collider-01.png",
                "cost": 50,
                "radius": 100,
                "link": ParticleCollider,
                "targetSize": 100,
            }
        ], areaPolygons);

        TowerManager.addEntropy(-1);
        TowerManager.addEntropy(levelData["startingEntropy"]);
        TowerManager.damageBase(-levelData["startingHealth"]);

        createThread(lambda _: (self.displayLevelPath(), self.startLevel(levelData['wavePath'])), None);