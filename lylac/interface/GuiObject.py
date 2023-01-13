import time
from typing import Literal
from lylac.interface.Instance import Instance
from lylac.interface.NominalObjects import SupportsOrdering
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties;
from lylac.modules.color4 import Color4;
from lylac.modules.udim2 import Udim2;
import lylac.modules.mathf as mathf;
import pygame

def calculate_rect_for_image(image: pygame.Surface, center: pygame.Vector2):
    x, y = center.xy;
    return image.get_rect(center = image.get_rect(center = (x, y)).center);

def rotateAroundCenter(image: pygame.Surface, angle: float, center: pygame.Vector2) -> tuple[pygame.Surface, pygame.Rect]:
    rotated_image = pygame.transform.rotozoom(image, -angle, 1);
    new_rect = calculate_rect_for_image(rotated_image, center);
    return (rotated_image, new_rect);

class GuiObject(Instance, SupportsOrdering):

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
    boundingRect: pygame.Rect;
    rotation: float;
    anchorPoint: pygame.Vector2;
    relativeSize: Literal['xx'] | Literal['xy'] | Literal['yy'];
    relativePosition: Literal['xx'] | Literal['xy'] | Literal['yy'];
    centerOfRotation: pygame.Vector2;

    surfaces: dict[Literal["dropShadowSurf"] | Literal["backgroundSurf"] | Literal["borderSurf"], tuple[pygame.Surface, pygame.Rect]];

    def __init__(self) -> None:
        self.surfaces = {};

        LoadDefaultGuiProperties('GuiObject', self);

        Instance.__init__(self);
        SupportsOrdering.__init__(self);


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

    def update_surfaces(self):

        self.update();

        size, position = self.absoluteSize, self.absolutePosition;

        dropOffset = self.udim2RelativeToSelfSize(self.dropShadowOffset, 'xx')

        dropPos = pygame.Vector2(position.x + dropOffset.x,
            position.y + dropOffset.y)

        dropSize = pygame.Vector2(size.x + self.dropShadowRadius,
            size.y + self.dropShadowRadius)

        dropNeonRect = pygame.Rect(dropPos, dropSize)
        backgroundRect = pygame.Rect(position.x, position.y, size.x, size.y)
        borderRect = pygame.Rect(position.x - self.borderWidth, position.y - self.borderWidth, size.x + self.borderWidth * 2, size.y + self.borderWidth * 2)
        
        dropShadowSurf = pygame.Surface((dropNeonRect.width, dropNeonRect.height), pygame.SRCALPHA, 32).convert_alpha();
        backgroundSurf = pygame.Surface((backgroundRect.width, backgroundRect.height), pygame.SRCALPHA, 32).convert_alpha();
        borderSurf = pygame.Surface((borderRect.width, borderRect.height), pygame.SRCALPHA, 32).convert_alpha();

        pygame.draw.rect(borderSurf, self.borderColor.toRGBATuple(), ((0, 0), borderRect.size), 0, border_radius=self.cornerRadius)

        pygame.draw.rect(backgroundSurf, self.backgroundColor.toRGBATuple(), ((0, 0), backgroundRect.size), 0, border_radius=self.cornerRadius)

        pygame.draw.rect(dropShadowSurf, self.dropShadowColor.toRGBATuple(), ((0, 0), dropNeonRect.size), border_radius=self.cornerRadius)
        
        center = pygame.Vector2(
            mathf.lerp(self.absolutePosition.x, self.absolutePosition.x + self.absoluteSize.x, self.centerOfRotation.x),
            mathf.lerp(self.absolutePosition.y, self.absolutePosition.y + self.absoluteSize.y, self.centerOfRotation.y)
        )

        dropCenter = pygame.Vector2(
            mathf.lerp(dropPos.x, dropPos.x + dropSize.x, self.centerOfRotation.x),
            mathf.lerp(dropPos.y, dropPos.y + dropSize.y, self.centerOfRotation.y)
        )

        (borderSurf, bdPos) = rotateAroundCenter(borderSurf, self.rotation, center);

        (backgroundSurf, bgPos) = rotateAroundCenter(backgroundSurf, self.rotation, center);

        (dropShadowSurf, dsPos) = rotateAroundCenter(dropShadowSurf, self.rotation, dropCenter);

        self.boundingRect = backgroundRect;

        self.surfaces['borderSurf'] = (borderSurf, bdPos);
        self.surfaces['dropShadowSurf'] = (dropShadowSurf, dsPos);
        self.surfaces['backgroundSurf'] = (backgroundSurf, bgPos);

    def recalculate_surface_positions_for_position_change(self):
        self.update();
        if len(self.surfaces) < 3: return;

        size, position = self.absoluteSize, self.absolutePosition;

        dropOffset = self.udim2RelativeToSelfSize(self.dropShadowOffset, 'xx')

        dropPos = pygame.Vector2(position.x + dropOffset.x,
            position.y + dropOffset.y)

        dropSize = pygame.Vector2(size.x + self.dropShadowRadius,
            size.y + self.dropShadowRadius)

        center = pygame.Vector2(
            mathf.lerp(self.absolutePosition.x, self.absolutePosition.x + self.absoluteSize.x, self.centerOfRotation.x),
            mathf.lerp(self.absolutePosition.y, self.absolutePosition.y + self.absoluteSize.y, self.centerOfRotation.y)
        )

        dropCenter = pygame.Vector2(
            mathf.lerp(dropPos.x, dropPos.x + dropSize.x, self.centerOfRotation.x),
            mathf.lerp(dropPos.y, dropPos.y + dropSize.y, self.centerOfRotation.y)
        )

        self.surfaces['borderSurf'] = (
            self.surfaces['borderSurf'][0], 
            calculate_rect_for_image(self.surfaces['borderSurf'][0], center)
        );
        self.surfaces['backgroundSurf'] = (
            self.surfaces['backgroundSurf'][0],
            calculate_rect_for_image(self.surfaces['backgroundSurf'][0], center)
        );
        
        self.surfaces['dropShadowSurf'] = (
            self.surfaces['dropShadowSurf'][0], 
            calculate_rect_for_image(self.surfaces['dropShadowSurf'][0], dropCenter)
        );
        
    def update(self):
        if not self.parent or not RenderService.rendererStarted: return;

        (position, size) = self.getSizeAndPositionFromUdim2(self.position, self.size);

        if size.x < 1 or size.y < 1: return;

        self.absolutePosition = position
        self.absoluteSize = size

        super().update()
    
    def render(self, dt: float):

        screen = RenderService.renderer.screen;
        
        if len(self.surfaces.keys()) < 3: return;

        (dropShadowSurf, dsPos) = self.surfaces['dropShadowSurf'];
        (borderSurf, bdPos) = self.surfaces['borderSurf'];
        (backgroundSurf, bgPos) = self.surfaces['backgroundSurf'];

        screen.blits([(dropShadowSurf, dsPos), (borderSurf, bdPos), (backgroundSurf, bgPos)]);


from lylac.services.RenderService import RenderService;