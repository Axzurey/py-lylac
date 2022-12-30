import json
import math
import time

from pygame import Vector2
from client.renderer import Renderer
from hooks.useActionState import useActionState
from interface.DraggableNurbsObject import DraggableNurbsObject
from interface.DraggablePolygonObject import DraggablePolygonObject
from interface.DraggableSegmentedLineObject import DraggableSegmentedLineObject
from interface.EmptyButton import EmptyButton
from interface.GuiObject import GuiObject
from interface.PolygonObject import PolygonObject
from interface.SegmentedLineObject import SegmentedLineObject
from interface.Sprite import Sprite
from interface.TextButton import TextButton
from modules.color4 import Color4
from modules.keymap import KeyCode
from modules.mathf import clamp
from modules.udim2 import Udim2
from modules.util import createThread
from services.AnimationService import AnimationService, InterpolationMode
from services.InputService import InputMouseBuffer, InputService
from services.RenderService import RenderService

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

with open('levels/grass_patch/towerAreas.json', 'r') as f:
    areas: list[list[list[float]]] = json.loads(f.read());
    polygons: list[PolygonObject] = [];

    for area in areas:
        a = PolygonObject(spr);
        a.color = Color4(1, 0, 0);
        a.points = [];
        for point in area:
            p = Vector2(point[0], point[1]);
            a.points.append(p);
        polygons.append(a);

    def checkPoly(x: InputMouseBuffer):
        print('checking poly')
        for poly in polygons:
            if poly.isPointInPolygon(x['position']):
                print('print in polygon');
                poly.color = Color4(0, 1, 0);
            else:
                poly.color = Color4(1, 0, 0);
    
    InputService.onMouseButton1Down.connect(checkPoly)

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
        print('NO POINT', t);
        return;

    s.position = Udim2.fromOffset(point.x, point.y)

RenderService.postRender.connect(upd)

mainRenderer.start(); #always goes at the bottom!