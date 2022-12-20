from typing import Literal
from interface.Instance import Instance
from interface.uifx import create_neon
from modules.defaultGuiProperties import LoadDefaultGuiProperties;
from modules.color4 import Color4;
from modules.udim2 import Udim2;
import modules.mathf as mathf;
import pygame

from services.RenderService import RenderService;

class GuiObject(Instance):

    size: Udim2;
    position: Udim2;
    backgroundColor: Color4;
    borderColor: Color4;
    borderWidth: int;
    dropShadowColor: Color4;
    dropShadowRadius: int;
    dropShadowOffset: Udim2;
    absolutePosition: pygame.Vector2;
    absoluteSize: pygame.Vector2;
    cornerRadius: int;
    zIndex: int;
    boundingRect: pygame.Rect;

    def __init__(self) -> None:
        super().__init__();
        LoadDefaultGuiProperties('GuiObject', self);

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
            
            return (position, size)
        
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

            return (position, size)

    def update(self, dt: float):

        screen = RenderService.renderer.screen;

        #background

        (position, size) = self.getSizeAndPositionFromUdim2(self.position, self.size)

        self.absolutePosition = position
        self.absoluteSize = size

        realSurf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        backgroundRect = pygame.Rect(position.x, position.y, size.x, size.y)

        borderRect = pygame.Rect(position.x - self.borderWidth, position.y - self.borderWidth, size.x + self.borderWidth * 2, size.y + self.borderWidth * 2)

        #borderSurf = pygame.Surface(borderRect.size, pygame.SRCALPHA)

        pygame.draw.rect(realSurf, self.borderColor.toRGBATuple(), borderRect, 0, border_radius=self.cornerRadius)

        pygame.draw.rect(realSurf, self.backgroundColor.toRGBATuple(), backgroundRect, 0, border_radius=self.cornerRadius)

        dropOffset = self.udim2RelativeToSelfSize(self.dropShadowOffset, 'xx')

        dropPos = pygame.Vector2(position.x + dropOffset.x,
            position.y + dropOffset.y)

        dropSize = pygame.Vector2(size.x + self.dropShadowRadius,
            size.y + self.dropShadowRadius)

        dropNeonRect = pygame.Rect(dropPos, dropSize)

        scrSize = screen.get_size()

        dropShadowSurface = pygame.Surface((scrSize[1], scrSize[0]), pygame.SRCALPHA)

        pygame.draw.rect(dropShadowSurface, self.dropShadowColor.toRGBTuple(), (dropNeonRect.y, dropNeonRect.x, dropNeonRect.h, dropNeonRect.w), border_radius=self.cornerRadius)

        dropNeonSurface = create_neon(dropShadowSurface)

        screen.blit(dropNeonSurface, (0, 0), special_flags = pygame.BLEND_PREMULTIPLIED)

        #screen.blit(borderSurf, borderRect)

        #screen.blit(backSurf, backgroundRect)

        screen.blit(realSurf, (0, 0), special_flags = pygame.BLEND_PREMULTIPLIED)

        self.boundingRect = backgroundRect

        super().update(dt)