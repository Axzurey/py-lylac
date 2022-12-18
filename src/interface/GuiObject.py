from interface.Instance import Instance
from modules.defaultGuiProperties import LoadDefaultGuiProperties;
from modules.color4 import Color4;
from modules.udim2 import Udim2;
import pygame;

class GuiObject(Instance):

    size: Udim2;
    position: Udim2;
    backgroundColor: Color4;
    borderColor: Color4;
    borderWidth: Color4;
    dropShadowColor: Color4;
    dropShadowRadius: int;
    dropShadowOffset: pygame.Vector2;
    absolutePosition: pygame.Vector2;
    absoluteSize: pygame.Vector2;
    cornerRadius: Udim2;
    zIndex: int;
    boundingRect: pygame.Rect;

    def __init__(self) -> None:
        super().__init__();
        LoadDefaultGuiProperties('GuiObject', self);

    def update(self, dt: float):
        pass