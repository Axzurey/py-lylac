from typing import Literal
from interface.GuiObject import GuiObject
from interface.TextObject import TextObject;
from modules.color4 import Color4
from modules.defaultGuiProperties import LoadDefaultGuiProperties;

class TextButton(TextObject):

    def __init__(self) -> None:
        super().__init__();
        LoadDefaultGuiProperties('TextButton', self);