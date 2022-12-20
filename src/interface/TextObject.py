from typing import Literal
from interface.GuiObject import GuiObject;
from modules.color4 import Color4
from modules.defaultGuiProperties import LoadDefaultGuiProperties;

class TextObject(GuiObject):
    text: str;
    textColor: Color4;
    textSize: int;
    textFont: str;
    textAlignX: Literal["right"] | Literal["center"] | Literal["left"];
    textAlignY: Literal["top"] | Literal["center"] | Literal["bottom"];

    def __init__(self) -> None:
        super().__init__();
        LoadDefaultGuiProperties('TextObject', self);