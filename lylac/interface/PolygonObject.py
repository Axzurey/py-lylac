import math
from math import cos, dist, sin, sqrt
import time
from typing import Iterator
from pygame import Vector2
import pygame
import pygame.gfxdraw
from lylac.client.renderer import Renderer
from lylac.interface.EmptyButton import EmptyButton
from lylac.interface.GuiObject import GuiObject;
from lylac.interface.Instance import Instance
from lylac.interface.NominalObjects import IsPolygonal
from lylac.modules.color4 import Color4
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties
from geomdl import utilities, NURBS
from lylac.modules.lylacSignal import LylacConnection
from lylac.modules.udim2 import Udim2
from lylac.services.InputService import InputService
from lylac.services.RenderService import RenderService

class PolygonObject(Instance, IsPolygonal):
    points: list[Vector2];
    color: Color4;
    width: int;

    partitions: list[list[tuple[float, float]]];

    showControlPoints: bool;
    controlPointColor: Color4;
    controlPointRadius: int;
    visible: bool = False;

    _surf: pygame.Surface | None = None;

    def __init__(self, parent: Instance | Renderer | None = None) -> None:
        Instance.__init__(self);
        IsPolygonal.__init__(self);

        LoadDefaultGuiProperties("PolygonObject", self);

        self.visible = False;

        self.partitions = [];

        self.parent = parent;

    def update(self):
        if not RenderService.rendererStarted: return;

        screen = RenderService.renderer.screen;

        size = screen.get_size();

        if self.parent and isinstance(self.parent, GuiObject):
            size = self.parent.absolutePosition.xy;
        
        surf = pygame.Surface(size, pygame.SRCALPHA, 32);
        surf = surf.convert_alpha()

        pointIndex = 0;
        for point in self.points:

            if self.showControlPoints:
                pygame.draw.circle(surf, self.controlPointColor.toRGBList(), point, self.controlPointRadius);

            if pointIndex == len(self.points) - 1:
                pygame.draw.line(surf, self.color.toRGBList(), point, self.points[0], int(self.width));
            else:
                pygame.draw.line(surf, self.color.toRGBList(), point, self.points[pointIndex + 1], int(self.width));
            pointIndex += 1;
    
        self._surf = surf;

    def render(self, dt: float):

        if not self._surf or not self.visible: return;

        screen = RenderService.renderer.screen;

        screen.blit(self._surf, (0, 0));