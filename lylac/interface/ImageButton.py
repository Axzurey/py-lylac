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

class ImageButton(GuiObject, Clickable, Hoverable):

    imagePath: str;

    surfaces: dict[Literal['image'], tuple[pygame.Surface, pygame.Rect]];

    _img: pygame.Surface | None = None;

    def __init__(self) -> None:
        
        GuiObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('ImageButton', self);

    def update_image(self):
        self._img = pygame.image.load(self.imagePath).convert_alpha();

        self.update()

    def update(self):
        
        if not self.parent or not self._img: return;

        img = pygame.transform.scale(self._img, self.absoluteSize);

        (img, imgPos) = rotateAroundCenter(img, self.rotation, self.absolutePosition + self.absoluteSize / 2);

        self.surfaces['image'] = (img, imgPos);

        super().update();


    def render(self, dt: float):
        super().render(dt);
        screen = RenderService.renderer.screen;
        
        if len(self.surfaces.keys()) < 4: return;

        (imageSurf, imageRect) = self.surfaces['image'];

        screen.blit(imageSurf, imageRect);