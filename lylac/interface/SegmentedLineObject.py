import math
from math import cos, dist, sin, sqrt
from typing import Iterator
from pygame import Vector2
import pygame
import pygame.gfxdraw
from lylac.client.renderer import Renderer
from lylac.interface.EmptyButton import EmptyButton
from lylac.interface.GuiObject import GuiObject;
from lylac.interface.Instance import Instance
from lylac.modules.color4 import Color4
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties
from geomdl import utilities, NURBS
from lylac.modules.lylacSignal import LylacConnection
from lylac.modules.mathf import lerp
from lylac.modules.udim2 import Udim2
from lylac.services.InputService import InputService
from lylac.services.RenderService import RenderService

class SegmentedLineObject(Instance):
    points: list[Vector2];
    color: Color4;
    width: int;

    partitions: list[list[tuple[float, float]]];

    showControlPoints: bool;
    controlPointColor: Color4;
    controlPointRadius: int;

    lineLength: float = 0;

    _surf: pygame.Surface | None = None;

    visible: bool = False;

    def __init__(self, parent: Instance | Renderer | None = None) -> None:
        super().__init__();

        LoadDefaultGuiProperties("SegmentedLineObject", self);

        self.partitions = [];

        self.parent = parent;

        self.visible = False;

    def getDeltaAlongLine(self, delta: float) -> None | Vector2:
        if delta == 0: return self.points[0];
        self.calculate_line_length();
        """
        Delta should be constrainted between the range [0, 1]. Values outside this range will be out of the line bounds.
        In such a case, the function will return None.
        """
        lengthTravelled = 0;
        requiredLengthToTravel = lerp(0, self.lineLength, delta);

        currentPointIndex = 0;
        while (lengthTravelled < requiredLengthToTravel):
            if currentPointIndex >= len(self.points) - 1: return None;
            point = self.points[currentPointIndex];
            nextPoint = self.points[currentPointIndex + 1];

            direction = nextPoint - point;
            magnitude = direction.magnitude();

            distanceLeft = requiredLengthToTravel - lengthTravelled;

            if distanceLeft <= magnitude:
                return point + direction.normalize() * distanceLeft;
            else:
                lengthTravelled += magnitude;
                currentPointIndex += 1;

    def calculate_line_length(self):
        l = 0;
        for i in range(len(self.points)):
            if i == len(self.points) - 1: break;

            l += (self.points[i] - self.points[i + 1]).magnitude();
        self.lineLength = l;
        return l;

    def update(self):

        if not RenderService.rendererStarted: return;

        screen = RenderService.renderer.screen;

        size = screen.get_size();

        if self.parent and isinstance(self.parent, GuiObject):
            size = self.parent.absoluteSize.xy;

        if not self.visible: return;
        
        surf = pygame.Surface(size, pygame.SRCALPHA, 32);
        surf = surf.convert_alpha()

        pointIndex = 0;
        for point in self.points:
            if self.showControlPoints:
                pygame.draw.circle(surf, self.controlPointColor.toRGBList(), point, self.controlPointRadius);
            
            if pointIndex == len(self.points) - 1: continue;

            pygame.draw.line(surf, self.color.toRGBList(), point, self.points[pointIndex + 1], self.width);
            pointIndex += 1;

        self._surf = surf;

    def render(self, dt: float):

        if not self._surf or not self.visible: return;

        screen = RenderService.renderer.screen;

        screen.blit(self._surf, (0, 0));