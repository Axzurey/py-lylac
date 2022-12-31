import json
import math
import time

from pygame import Vector2
from custom.towerWidget import TowerWidget
from lylac import *

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
spr.imagePath = "assets/environment/grass patch-01.png";
spr.parent = frame;
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

def checkPoly(x: InputMouseBuffer):
    for poly in areaPolygons:
        if poly.isPointInPolygon(x['position']):
            poly.color = Color4(0, 1, 0);
        else:
            poly.color = Color4(1, 0, 0);

def checkContext():
    ...

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

InputService.onMouseButton1Down.connect(checkPoly)


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
        print('NO POINT', t);
        return;

    s.position = Udim2.fromOffset(point.x, point.y)

RenderService.postRender.connect(upd);

towerWidget = TowerWidget(spr, [])

mainRenderer.start(); #always goes at the bottom!

#TODO: clicking near the corner of a frame doesn't seem to be accurate anymore.