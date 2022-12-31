from typing import Literal
from lylac.interface.GuiObject import GuiObject
from lylac.interface.NominalObjects import Clickable, Hoverable
from lylac.interface.TextObject import TextObject;
from lylac.modules.color4 import Color4
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties
from lylac.modules.lylacSignal import LylacSignal;

class EmptyButton(GuiObject, Clickable, Hoverable):

    def __init__(self) -> None:
        GuiObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('EmptyButton', self);

    def update(self):
        super().update();

    def render(self, dt: float):
        super().render(dt);