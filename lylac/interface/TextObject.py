from typing import Literal
from lylac.interface.GuiObject import GuiObject;
from lylac.modules.color4 import Color4
from lylac.services.FontService import FontService, FreeFont;
from lylac.services.RenderService import RenderService
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties;

def getFontWrap(text: str, font: str, fontSize: int, maxWidth: int) -> tuple[list[str], list[int]]:
    """
    Returns an array consisting of the lines and an array consisting of required Vertical spacing between the lines
    """
    words = text.split(' ');

    splitLines: list[list[str]] = [];
    lineSpacings: list[int] = [];
    sentences: list[str] = [];

    currentLineWidth = 0;
    splitLineObject = [];
    for word in words:
        fw, _fh = FontService.get_width_and_height_for_string(font, word + " ", fontSize);
        if currentLineWidth + fw > maxWidth: #this should account for the spaces that will be added later.
            currentLineWidth = 0;
            splitLines.append(splitLineObject);
            splitLineObject = [];
            splitLineObject.append(word);
            currentLineWidth += fw;
        else:
            splitLineObject.append(word);
            currentLineWidth += fw;

    if not splitLineObject in splitLines:
        splitLines.append(splitLineObject);

    for splitLine in splitLines:
        newLine = ' '.join(splitLine);
        sentences.append(newLine);
        _fw, fh = FontService.get_width_and_height_for_string(font, newLine, fontSize);
        lineSpacings.append(fh);

    return sentences, lineSpacings;

class TextObject(GuiObject):
    text: str;
    textColor: Color4;
    textSize: int;
    textFont: str;
    textAlignX: Literal["right"] | Literal["center"] | Literal["left"];
    textAlignY: Literal["top"] | Literal["center"] | Literal["bottom"];
    wrapText: bool = True;

    def __init__(self) -> None:
        super().__init__();
        LoadDefaultGuiProperties('TextObject', self);

    def update(self):
        super().update();
    def render(self, dt: float):
        super().render(dt);
        self.renderText();

    def renderText(self):

        renderer = RenderService.renderer;

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

        lines, spacing = getFontWrap(self.text, self.textFont, self.textSize, int(self.absoluteSize.x) if self.wrapText else 999999);

        lineIndex = 0;
        for line in lines:

            (textSurf, _) = FontService.fonts[self.textFont].render(line, self.textColor.toRGBATuple(), size=self.textSize)

            textSize = textSurf.get_size()

            absSize = self.absoluteSize
            absPos = self.absolutePosition
            
            offsetXAbs = absPos.x + (absSize.x - textSize[0]) * textOffsetX
            offsetYAbs = absPos.y + (absSize.y - textSize[1]) * textOffsetY + spacing[lineIndex] * lineIndex
            lineIndex += 1;

            renderer.screen.blit(textSurf, (offsetXAbs, offsetYAbs))