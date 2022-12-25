import math
import time

from pygame import Vector2
from client.renderer import Renderer
from hooks.useActionState import useActionState
from interface.CNurbsObject import CNurbsObject
from interface.EmptyButton import EmptyButton
from interface.GuiObject import GuiObject
from interface.NurbsObject import NurbsObject
from interface.Sprite import Sprite
from interface.TextButton import TextButton
from modules.color4 import Color4
from modules.keymap import KeyCode
from modules.udim2 import Udim2
from modules.util import createThread
from services.InputService import InputService
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

curve = CNurbsObject(frame);

btn = EmptyButton();
btn.position = Udim2.fromOffset(700, 500);
btn.size = Udim2.fromOffset(50, 50);
btn.parent = frame;
btn.onMouseButton1Down.connect(lambda _: curve.createPoint(Vector2(500, 400)));

spr = Sprite();
spr.imagePath = "C:\\Users\\Phxie\\Pictures\\unknown.png";
spr.parent = frame;
spr.size = Udim2.fromOffset(15, 15);
spr.position = Udim2(.2, .2);

def toggle(t: bool):
    if t: 
        spr.imagePath = "C:\\Users\\Phxie\\Pictures\\unknown.png";
    else:
        spr.imagePath = "C:\\Users\\Phxie\\Pictures\\unknown2.png";

spr.onMouseButton1Up.connect(lambda _: toggle(True));
spr.onMouseButton1Down.connect(lambda _: toggle(False));

t = 0;

def upd(_):
    global t;
    t += 1;

    if t >= len(curve.curvePoints) - 1:
        global updSPR;
        updSPR.disconnect();
        return;

    s = curve.curvePoints[t];

    spr.position = Udim2.fromOffset(s[0] - 15 / 2, s[1] - 15 / 2);

updSPR = RenderService.postRender.connect(upd)

InputService.onKeyDown.connect(lambda b: print(b['key']));

mainRenderer.start(); #always goes at the bottom!