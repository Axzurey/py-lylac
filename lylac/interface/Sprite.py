from typing import Literal
from pygame import Vector2
import pygame
from lylac.interface.GuiObject import calculate_rect_for_image, rotateAroundCenter
from lylac.interface.Instance import Instance
from lylac.interface.NominalObjects import Clickable, Hoverable, SupportsOrdering
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties
from lylac.modules.udim2 import Udim2
import lylac.modules.mathf as mathf
from lylac.services.RenderService import RenderService;
from cachetools import cached;
from cachetools.keys import hashkey;

preloaded_images: dict[str, pygame.Surface] = {

}

@cached(cache={}, key=lambda imagePath, _absolutePosition, _absoluteSize, _rotation: hashkey(imagePath, _absoluteSize, _rotation))
def get_image(imagePath: str, _absolutePosition: tuple[int, int], _absoluteSize: tuple[int, int], rotation: int):
    absoluteSize = pygame.Vector2(_absoluteSize);
    absolutePosition = pygame.Vector2(_absolutePosition);

    _img = pygame.image.load(imagePath).convert_alpha() if imagePath not in preloaded_images else preloaded_images[imagePath];
    preloaded_images[imagePath] = _img;

    img = pygame.transform.scale(_img, absoluteSize);

    (img, imgPos) = rotateAroundCenter(img, rotation, absolutePosition + absoluteSize / 2);

    return img, (img, imgPos);

class Sprite(Instance, SupportsOrdering, Clickable, Hoverable):

    size: Udim2;
    position: Udim2;
    absoluteSize: Vector2;
    absolutePosition: Vector2;
    rotation: int;
    boundingRect: pygame.Rect;
    imagePath: str;
    anchorPoint: Vector2;
    relativeSize: Literal['xx'] | Literal['xy'] | Literal['yy'];
    relativePosition: Literal['xx'] | Literal['xy'] | Literal['yy'];
    canHover: bool;

    surfaces: dict[Literal['image'], tuple[pygame.Surface, pygame.Rect]];

    _img: pygame.Surface | None = None;
    
    def __init__(self) -> None:
        Instance.__init__(self);
        SupportsOrdering.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties("Sprite", self);

        self.surfaces = {};

    def udim2RelativeToSelfSize(self, udim: Udim2, relative: Literal['xx'] | Literal['xy'] | Literal['yy'] = 'xy'):

        size = self.absoluteSize

        fS = udim.toScale()
        fsO = udim.toOffset()

        size = pygame.Vector2(mathf.lerp(0, size.x, fS.x) + fsO.x, mathf.lerp(0, size.y, fS.y) + fsO.y)

        if relative == 'xx':
            size.y = size.x
        elif relative == 'yy':
            size.x = size.y
        
        return size

    def getSizeAndPositionFromUdim2(self, positionUdim: Udim2, sizeUdim: Udim2):
        """
        Returns: (position, size)
        """
        if self.parent and isinstance(self.parent, Instance):
            pPos = self.parent.absolutePosition
            pSize = self.parent.absoluteSize

            fP = positionUdim.toScale()
            fpO = positionUdim.toOffset()
            fS = sizeUdim.toScale()
            fsO = sizeUdim.toOffset()

            position = pygame.Vector2(mathf.lerp(pPos.x, pPos.x + pSize.x, fP.x) + fpO.x, mathf.lerp(pPos.y, pPos.y + pSize.y, fP.y) + fpO.y)
            size = pygame.Vector2(mathf.lerp(0, pSize.x, fS.x) + fsO.x, mathf.lerp(0, pSize.y, fS.y) + fsO.y)

            if self.relativeSize == "xx":
                size = pygame.Vector2(size.x, size.x);
            elif self.relativeSize == "yy":
                size = pygame.Vector2(size.y, size.y);
            if self.relativePosition == "xx":
                position = pygame.Vector2(position.x, position.x);
            elif self.relativePosition == "yy":
                position = pygame.Vector2(position.y, position.y);

            position -= size.elementwise() * self.anchorPoint.elementwise();

            return (position, pygame.Vector2(mathf.clamp(0, size.x, size.x), mathf.clamp(0, size.y, size.y)))
        
        else:
            container = RenderService.renderer.resolution

            pPos = pygame.Vector2(0, 0)
            pSize = pygame.Vector2(container[0], container[1])

            fP = positionUdim.toScale()
            fpO = positionUdim.toOffset()
            fS = sizeUdim.toScale()
            fsO = sizeUdim.toOffset()

            position = pygame.Vector2(mathf.lerp(pPos.x, pPos.x + pSize.x, fP.x) + fpO.x, mathf.lerp(pPos.y, pPos.y + pSize.y, fP.y) + fpO.y)
            size = pygame.Vector2(mathf.lerp(0, pSize.x, fS.x) + fsO.x, mathf.lerp(0, pSize.y, fS.y) + fsO.y)

            if self.relativeSize == "xx":
                size = pygame.Vector2(size.x, size.x);
            elif self.relativeSize == "yy":
                size = pygame.Vector2(size.y, size.y);
            if self.relativePosition == "xx":
                position = pygame.Vector2(position.x, position.x);
            elif self.relativePosition == "yy":
                position = pygame.Vector2(position.y, position.y);

            position -= size.elementwise() * self.anchorPoint.elementwise();

            return (position, pygame.Vector2(mathf.clamp(0, size.x, size.x), mathf.clamp(0, size.y, size.y)))

    def render(self, dt: float):
        screen = RenderService.renderer.screen;
        if len(self.surfaces.keys()) < 1: return;

        (imageSurf, imageRect) = self.surfaces['image'];

        screen.blit(imageSurf, imageRect);

    def update_image(self):
        #self._img = pygame.image.load(self.imagePath).convert_alpha();

        #img = pygame.transform.scale(self._img, self.absoluteSize)

        #(img, imgPos) = rotateAroundCenter(img, self.rotation, self.absolutePosition + self.absoluteSize / 2);

        _img, (img, imgPos) = get_image(self.imagePath, (self.absolutePosition.x, self.absolutePosition.y), (self.absoluteSize.x, self.absoluteSize.y), self.rotation); #type: ignore
        self._img = _img;
        self.surfaces['image'] = (img, imgPos);
        self.recalculate_surface_positions_for_position_change();

    def recalculate_surface_positions_for_position_change(self):
        self.update();

        if len(self.surfaces) < 1: return;

        self.surfaces['image'] = (
            self.surfaces['image'][0],
            calculate_rect_for_image(self.surfaces['image'][0], self.absolutePosition + self.absoluteSize / 2)
        );

    def update(self):
        
        if not self.parent or not self._img: return;

        (position, size) = self.getSizeAndPositionFromUdim2(self.position, self.size);

        if size.x < 1 or size.y < 1: return;

        self.absolutePosition = position;
        self.absoluteSize = size;

        return super().update();