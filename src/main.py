from client.renderer import Renderer
from interface.GuiObject import GuiObject
from interface.TextButton import TextButton
from modules.color4 import Color4
from modules.keymap import KeyCode
from modules.udim2 import Udim2
from services.InputService import InputService

mainRenderer = Renderer((700, 350), 60);

frame = GuiObject()
frame.parent = mainRenderer;

frame.borderWidth = 2;
frame.size = Udim2.fromOffset(200, 300);
frame.backgroundColor = Color4(0, 1, 1, 1);
frame.position = Udim2.fromScale(.25, .25);
frame.borderColor = Color4(1, 1, 1)
frame.dropShadowOffset = Udim2.fromOffset(5, 5);

btn2 = TextButton()
btn2.text = 'Y'
btn2.zindex = 13
btn2.textAlignX = 'center'
btn2.textAlignY = 'center'
btn2.textSize = 40
btn2.parent = frame
btn2.position = Udim2(0, .4, 0, .4)
btn2.size = Udim2.fromOffset(150, 100)
btn2.cornerRadius = 45

btn2.onMouseButton1Down.connect(lambda _: print('clicked!'));
btn2.onMouseButton1Up.connect(lambda _: print('raised'));
btn2.onHoverEnter.connect(lambda _: print('enter'));
btn2.onHoverExit.connect(lambda _: print('leave'));

InputService.onKeyDown.connect(lambda b: print(b['key']))

mainRenderer.start(); #always goes at the bottom!