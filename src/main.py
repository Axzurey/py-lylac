from client.renderer import Renderer
from interface.GuiObject import GuiObject
from modules.color4 import Color4
from modules.keymap import LylacEnum
from modules.udim2 import Udim2
from services.InputService import InputService

mainRenderer = Renderer((1280, 720), 60);

frame = GuiObject()
frame.parent = mainRenderer;

frame.borderWidth = 2;
frame.size = Udim2.fromOffset(700, 300);
frame.backgroundColor = Color4(0, 1, 1, 1);
frame.position = Udim2.fromScale(.25, .25);
frame.borderColor = Color4(1, 1, 1)
frame.dropShadowOffset = Udim2.fromOffset(5, 5)

InputService.onKeyDown.connect(lambda b: print(b['key']))

mainRenderer.start(); #always goes at the bottom!