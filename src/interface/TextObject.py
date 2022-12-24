from typing import Literal
from interface.GuiObject import GuiObject;
from modules.color4 import Color4
from services.FontService import FontService
from services.RenderService import RenderService
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

    def update(self):
        super().update();
    def render(self, dt: float):
        super().render(dt);

    def renderText(self):

        renderer = RenderService.renderer;

        (textSurf, _) = FontService.fonts[self.textFont].render(self.text, self.textColor.toRGBATuple(), size=self.textSize)

        textOffsetX = 0
        textOffsetY = 0

        if self.textAlignX == 'right':
            textOffsetX = 1
        elif self.textAlignX == 'center':
            textOffsetX = .5
        else:
            textOffsetX = 0

        if self.textAlignY == 'bottom':
            textOffsetY = 1
        elif self.textAlignY == 'center':
            textOffsetY = .5
        else:
            textOffsetY = 0

        textSize = textSurf.get_size()

        absSize = self.absoluteSize
        absPos = self.absolutePosition
        
        offsetXAbs = absPos.x + (absSize.x - textSize[0]) * textOffsetX
        offsetYAbs = absPos.y + (absSize.y - textSize[1]) * textOffsetY

        renderer.screen.blit(textSurf, (offsetXAbs, offsetYAbs))