import math
import time

from pygame import Vector2
from client.renderer import Renderer
from hooks.useActionState import useActionState
from interface.CNurbsObject import CNurbsObject
from interface.GuiObject import GuiObject
from interface.NurbsObject import NurbsObject
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

curve = CNurbsObject(mainRenderer);
#TODO: DRAGGING IS A BIT... OFF

InputService.onKeyDown.connect(lambda b: print(b['key']))

mainRenderer.start(); #always goes at the bottom!