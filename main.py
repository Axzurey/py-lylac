import json
import math
import time

from pygame import Vector2
from custom.towerWidget import TowerWidget
from data.towers.StarBlue import StarBlue
from lylac import *
from lylac.services.DebugService import DebugService

mainRenderer = Renderer((1280, 720), 60);

frame = GuiObject()
frame.parent = mainRenderer;
frame.borderWidth = 2;
frame.size = Udim2.fromOffset(1280, 720);
frame.backgroundColor = Color4(0, 1, 1);
frame.position = Udim2.fromOffset(0, 0);
frame.borderColor = Color4(1, 1, 1)
frame.dropShadowOffset = Udim2.fromOffset(5, 5);

spr = Sprite();
spr.parent = frame;
spr.imagePath = "assets/environment/grass patch-01.png";
spr.size = Udim2.fromOffset(1280, 720);
spr.position = Udim2();

with open('levels/grass_patch/enemyPath.json', 'r') as f:
    path: list[list[float]] = json.loads(f.read());
    
    curve = SegmentedLineObject(spr);
    curve.color = Color4(0, 1, 1)
    curve.points = [];
    
    for point in path:
        v = Vector2(point[0], point[1]);
        curve.points.append(v);
    f.close();

areaPolygons: list[PolygonObject] = [];

with open('levels/grass_patch/towerAreas.json', 'r') as f:
    areas: list[list[list[float]]] = json.loads(f.read());

    for area in areas:
        a = PolygonObject(spr);
        a.color = Color4(1, 0, 0);
        a.points = [];
        for point in area:
            p = Vector2(point[0], point[1]);
            a.points.append(p);
        areaPolygons.append(a);
    f.close();

s = Sprite();
s.imagePath = "assets/asteroid.png";
s.parent = frame;
s.anchorPoint = Vector2(.5, .5)
s.size = Udim2.fromOffset(20, 20);
s.position = Udim2();

t = 0;
def upd(dt: float):
    global curve;
    global t;
    t = clamp(0, 1, t + dt / 25);

    if t >= 1: return;
    point = curve.getDeltaAlongLine(t);

    if not point:
        return;

    s.position = Udim2.fromOffset(point.x, point.y)

RenderService.postRender.connect(upd);

towerWidget = TowerWidget(spr, [
    {
        "name": "Star Blue",
        "imagePath": "assets/towers/star-blue.png",
        "cost": 100,
        "radius": 200,
        "link": StarBlue
    },
    {
        "name": "Eclipse Red",
        "imagePath": "assets/towers/star-blue.png",
        "cost": 150,
        "radius": 250,
        "link": StarBlue
    }
], areaPolygons);

mainRenderer.start(); #always goes at the bottom!

#TODO: clicking near the corner of a frame doesn't seem to be accurate anymore.