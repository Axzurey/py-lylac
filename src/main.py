from client.renderer import Renderer
from interface.GuiObject import GuiObject
from modules.color4 import Color4
from modules.udim2 import Udim2

mainRenderer = Renderer((1280, 720), 60);

frame = GuiObject()
frame.parent = mainRenderer;

frame.borderWidth = 2;
frame.size = Udim2.fromOffset(700, 300);
frame.backgroundColor = Color4(0, 1, 1, 1);
frame.position = Udim2.fromScale(.25, .25);
frame.borderColor = Color4(1, 1, 1)
frame.dropShadowOffset = Udim2.fromOffset(5, 5)

mainRenderer.start(); #always goes at the bottom!