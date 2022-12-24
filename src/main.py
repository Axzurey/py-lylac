import math
import time

from pygame import Vector2
from client.renderer import Renderer
from interface.GuiObject import GuiObject
from interface.TextButton import TextButton
from modules.color4 import Color4
from modules.keymap import KeyCode
from modules.udim2 import Udim2
from modules.util import createThread
from services.InputService import InputService

mainRenderer = Renderer((1280, 720), 60);

frame = GuiObject()
frame.parent = mainRenderer;

frame.borderWidth = 2;
frame.size = Udim2.fromOffset(200, 300);
frame.backgroundColor = Color4(0, 1, 1, 1);
frame.position = Udim2.fromOffset(100, 100);
frame.borderColor = Color4(1, 1, 1)
frame.dropShadowOffset = Udim2.fromOffset(5, 5);

btn2 = GuiObject()
btn2.zindex = 13
btn2.parent = frame
btn2.backgroundColor = Color4(1, 1, 0)
btn2.borderColor = Color4(0, 1, 0)
btn2.position = Udim2(200, 0, 200, 0)
btn2.size = Udim2.fromOffset(150, 150)
btn2.cornerRadius = 0
btn2.rotation = 45;

btn2 = TextButton()
btn2.text = 'Y'
btn2.zindex = 13
btn2.textAlignX = 'center'
btn2.textAlignY = 'center'
btn2.textSize = 40
btn2.parent = frame
btn2.backgroundColor = Color4(1, 0, 0)
btn2.borderColor = Color4(0, 1, 0)
btn2.position = Udim2(200, 0, 200, 0)
btn2.size = Udim2.fromOffset(150, 150)
btn2.cornerRadius = 45
btn2.rotation = 75;

#btn2.onMouseButton1Down.connect(lambda _: print('clicked!'));
#btn2.onMouseButton1Up.connect(lambda _: print('raised'));
btn2.onHoverEnter.connect(lambda _: print('enter'));
btn2.onHoverExit.connect(lambda _: print('leave'));

InputService.onKeyDown.connect(lambda b: print(b['key']))

mainRenderer.start(); #always goes at the bottom!

#TODO: framerate seems VERY VERY LOW. Find out what's taking it up