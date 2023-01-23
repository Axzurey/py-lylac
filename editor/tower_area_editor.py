import json
import math
import time

from pygame import Vector2
from lylac import *

mainRenderer = Renderer("Blue Storm Test place c:", (1280, 720), 60);

frame = GuiObject()
frame.parent = mainRenderer;
frame.borderWidth = 2;
frame.size = Udim2.fromOffset(1280, 720);
frame.backgroundColor = Color4(0, 1, 1);
frame.position = Udim2.fromOffset(0, 0);
frame.borderColor = Color4(1, 1, 1)
frame.dropShadowOffset = Udim2.fromOffset(5, 5);

spr = Sprite();
spr.imagePath = "assets/environment/aqua stage-01.png";
spr.parent = frame;
spr.size = Udim2.fromOffset(1280, 720);
spr.position = Udim2(0, 0);

curve = DraggablePolygonObject(spr);
curve.color = Color4(0, 1, 1)

btn = TextButton();
btn.position = Udim2.fromOffset(700, 500);
btn.size = Udim2.fromOffset(100, 50);
btn.textSize = 12;
btn.text = "Create Vertex";
btn.parent = frame;
btn.textAlignX = "center";
btn.textAlignY = "center";
btn.onMouseButton1Down.connect(lambda _: (curve.createPoint(Vector2(500, 400))));

bt2 = TextButton();
bt2.position = Udim2.fromOffset(1000, 400);
bt2.size = Udim2.fromOffset(100, 50);
bt2.parent = frame;
bt2.textSize = 24;
bt2.textAlignX = "center";
bt2.textAlignY = "center";
bt2.text = "SAVE";

def save():

    f = open("towerAreas.json", "r");
    js: list[list[float]] = json.loads(f.read());
    f.close();
    t = [];

    for point in curve.points:
            t.append([point.x, point.y]);

    js.append(t)

    with open("towerAreas.json", "w") as file:
        file.write(json.dumps(js, indent=4));

    print('saved')

bt2.onMouseButton1Down.connect(lambda _: save());

mainRenderer.start(); #always goes at the bottom!