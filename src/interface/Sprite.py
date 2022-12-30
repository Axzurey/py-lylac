from typing import Literal
from pygame import Vector2
import pygame
from interface.GuiObject import rotateAroundCenter
from interface.Instance import Instance
from interface.NominalObjects import Clickable, Hoverable, SupportsOrdering
from modules.defaultGuiProperties import LoadDefaultGuiProperties
from modules.udim2 import Udim2
import modules.mathf as mathf
from services.RenderService import RenderService;


class Sprite(Instance, SupportsOrdering, Clickable, Hoverable):

    size: Udim2;
    position: Udim2;
    absoluteSize: Vector2;
    absolutePosition: Vector2;
    rotation: int;
    boundingRect: pygame.Rect;
    imagePath: str;
    anchorPoint: Vector2; #TODO: IMPLEMENT THIS

    surfaces: dict[Literal['image'], tuple[pygame.Surface, pygame.Rect]];
    
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

            position -= size.elementwise() * self.anchorPoint.elementwise();

            return (position, pygame.Vector2(mathf.clamp(0, size.x, size.x), mathf.clamp(0, size.y, size.y)))

    def render(self, dt: float):
        screen = RenderService.renderer.screen;

        if len(self.surfaces.keys()) < 1: return;

        (imageSurf, imageRect) = self.surfaces['image'];

        screen.blit(imageSurf, imageRect, special_flags=pygame.BLEND_PREMULTIPLIED);

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