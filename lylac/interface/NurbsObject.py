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
from lylac.modules.udim2 import Udim2
from lylac.services.InputService import InputService
from lylac.services.RenderService import RenderService

def evenly_split(
    curve: NURBS.Curve,
    distance: float,
    include_last: bool = True,
    du: float = 1,
    iterations: int = 1,
) -> Iterator[list[float]]:
    u = 0
    y = curve.evaluate_single(0)
    yield y.copy()
    while u + du <= 1:
        for _ in range(iterations):
            du *= sqrt(distance / dist(curve.evaluate_single(u + du), y))
            if u + du > 1:
                break
        else:
            u += du
            y = curve.evaluate_single(u)
            yield y.copy()
    if include_last:
        yield curve.evaluate_single(1)

class NurbsObject(Instance):
    points: list[Vector2];
    color: Color4;
    width: float;

    partitions: list[list[tuple[float, float]]];

    curvePoints: list[list[float]] = [];
    
    showControlPoints: bool;
    controlPointColor: Color4;
    controlPointRadius: int;

    _surf: pygame.Surface | None = None;

    def __init__(self, parent: Instance | Renderer | None = None) -> None:
        super().__init__();

        LoadDefaultGuiProperties("NurbsObject", self);

        self.partitions = [];

        self.parent = parent;

    def drawLineAA(self, a: Vector2, b: Vector2):
        #https://stackoverflow.com/questions/30578068/pygame-draw-anti-aliased-thick-line
        center_L1 = (a + b) / 2.

        length = (a - b).magnitude()
        thickness = self.width
        angle = math.atan2(a[1] - b[1], a[0] - b[0]);

        UL = (center_L1[0] + (length/2.) * cos(angle) - (thickness/2.) * sin(angle),
            center_L1[1] + (thickness/2.) * cos(angle) + (length/2.) * sin(angle))
        UR = (center_L1[0] - (length/2.) * cos(angle) - (thickness/2.) * sin(angle),
            center_L1[1] + (thickness/2.) * cos(angle) - (length/2.) * sin(angle))
        BL = (center_L1[0] + (length/2.) * cos(angle) + (thickness/2.) * sin(angle),
            center_L1[1] - (thickness/2.) * cos(angle) + (length/2.) * sin(angle))
        BR = (center_L1[0] - (length/2.) * cos(angle) + (thickness/2.) * sin(angle),
            center_L1[1] - (thickness/2.) * cos(angle) - (length/2.) * sin(angle))

        return [UL, UR, BL, BR];

    def update(self):
        if not RenderService.rendererStarted: return;

        curve = NURBS.Curve()

        # Set up the curve
        curve.degree = len(self.points) - 1;
        curve.ctrlpts = [[v.x, v.y] for v in self.points];

        # Auto-generate knot vector
        curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

        # Set evaluation delta
        curve.delta = 0.01;

        # Evaluate curve

        points: list[Vector2] = list(evenly_split(curve, .5)); #type: ignore (I really don't give a shit)

        finalPoints: list[list[tuple[float, float]]] = [];

        self.curvePoints = points; #type: ignore

        pointIndex = 0;
        for point in points:
            if pointIndex == len(points) - 1: continue;

            #pygame.draw.line(surf, (0, 255, 255), point, points[pointIndex + 1], 15)
            res = self.drawLineAA(pygame.Vector2(point), pygame.Vector2(points[pointIndex + 1]));
            finalPoints.append(res);

            pointIndex += 1;

        self.partitions = finalPoints;

        screen = RenderService.renderer.screen;

        size = screen.get_size();

        if self.parent and isinstance(self.parent, GuiObject):
            size = self.parent.absolutePosition.xy;
        
        surf = pygame.Surface(size, pygame.SRCALPHA, 32);
        surf = surf.convert_alpha()

        if self.showControlPoints:
            for point in self.points:
                pygame.draw.circle(surf, self.controlPointColor.toRGBList(), point, self.controlPointRadius);

        for point in self.partitions:
            (UL, UR, BR, BL) = point;
            pygame.gfxdraw.aapolygon(surf, (UL, UR, BR, BL), self.color.toRGBATuple())
            pygame.gfxdraw.filled_polygon(surf, (UL, UR, BR, BL), self.color.toRGBATuple())

        self._surf = surf;

    def render(self, dt: float):

        if not self._surf: return;

        screen = RenderService.renderer.screen;

        screen.blit(self._surf, (0, 0));