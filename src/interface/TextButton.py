from typing import Literal
from interface.GuiObject import GuiObject
from interface.NominalObjects import Clickable, Hoverable
from interface.TextObject import TextObject;
from modules.color4 import Color4
from modules.defaultGuiProperties import LoadDefaultGuiProperties
from modules.lylacSignal import LylacSignal;

class TextButton(TextObject, Clickable, Hoverable):

    enabled: bool = False;

    def __init__(self) -> None:
        TextObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('TextButton', self);

    def update(self, dt: float):
        super().update(dt)
        self.renderText()