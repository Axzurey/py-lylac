from lylac.interface.GuiObject import GuiObject
from lylac.interface.NominalObjects import Clickable, Hoverable
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties


class Frame(GuiObject, Clickable, Hoverable):
    def __init__(self) -> None:
        GuiObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('Frame', self);