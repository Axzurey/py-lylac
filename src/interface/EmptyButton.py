from typing import Literal
from interface.GuiObject import GuiObject
from interface.NominalObjects import Clickable, Hoverable
from interface.TextObject import TextObject;
from modules.color4 import Color4
from modules.defaultGuiProperties import LoadDefaultGuiProperties
from modules.lylacSignal import LylacSignal;

class EmptyButton(GuiObject, Clickable, Hoverable):

    enabled: bool = False;

    def __init__(self) -> None:
        GuiObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('EmptyButton', self);

    def update(self):
        super().update();

    def render(self, dt: float):
        super().render(dt);