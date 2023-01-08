import json
from typing import TypedDict

from pygame import Vector2
from custom.LevelSelector import LevelData
from data.Enemy import EnemyManager
import lylac

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

    def __init__(self, screen: lylac.Renderer, levelData: LevelData) -> None:
        spr = lylac.Sprite();
        spr.parent = screen;
        spr.imagePath = levelData['backdrop'];
        spr.size = lylac.Udim2.fromOffset(1280, 720);
        spr.position = lylac.Udim2();

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