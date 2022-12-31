from typing import Literal

import pygame
from lylac.interface.GuiObject import GuiObject
from lylac.interface.NominalObjects import Clickable, Hoverable
from lylac.interface.TextObject import TextObject
from lylac.interface.GuiObject import rotateAroundCenter
from lylac.services.RenderService import RenderService;
from lylac.modules.color4 import Color4
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties
from lylac.modules.lylacSignal import LylacSignal;

class ImageButton(TextObject, Clickable, Hoverable):

    imagePath: str;

    surfaces: dict[Literal['image'], tuple[pygame.Surface, pygame.Rect]];

    def __init__(self) -> None:
        TextObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('ImageButton', self);

        self.surfaces = {};

    def update(self):
        
        if not self.parent or not RenderService.rendererStarted: return;

        (position, size) = self.getSizeAndPositionFromUdim2(self.position, self.size);

        self.absolutePosition = position;
        self.absoluteSize = size;

        img = pygame.image.load(self.imagePath).convert_alpha();

        img = pygame.transform.scale(img, size);

        (img, imgPos) = rotateAroundCenter(img, self.rotation, position + size / 2);

        self.surfaces['image'] = (img, imgPos);

        return super().update();

    def render(self, dt: float):
        super().render(dt);
        screen = RenderService.renderer.screen;

        if len(self.surfaces.keys()) < 1: return;

        (imageSurf, imageRect) = self.surfaces['image'];

        screen.blit(imageSurf, imageRect, special_flags=pygame.BLEND_PREMULTIPLIED);