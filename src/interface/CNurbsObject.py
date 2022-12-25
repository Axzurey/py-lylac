import math
from math import cos, sin
from pygame import Vector2
import pygame
import pygame.gfxdraw
from client.renderer import Renderer
from interface.EmptyButton import EmptyButton;
from interface.Instance import Instance
from modules.color4 import Color4
from modules.defaultGuiProperties import LoadDefaultGuiProperties
from geomdl import BSpline, utilities
from modules.udim2 import Udim2
from services.InputService import InputService

from services.RenderService import RenderService

#https://nurbs-python.readthedocs.io/en/5.x/basics.html

class CNurbsObject(Instance):
    points: list[Vector2];
    color: Color4;
    width: float;
    pointButtons: list[EmptyButton];

    partitions: list[list[tuple[float, float]]];

    def __init__(self, parent: Instance | Renderer | None = None) -> None:
        super().__init__();

        self.partitions = [];

        LoadDefaultGuiProperties("CNurbsObject", self);

        self.parent = parent;

        def startPointListening(btn: EmptyButton, index: int):
            print('clickd')
            def cancelStep(_):
                nonlocal c1;
                nonlocal c2;
                c1.disconnect();
                c2.disconnect();

            def updatePos(_):

                mousePos = InputService.getMousePosition();

                self.points[index] = mousePos;
                btn.position = Udim2.fromOffset(mousePos.x + 15 / 2, mousePos.x + 15 / 2)

            c1 = RenderService.postRender.connect(updatePos);

            c2 = btn.onMouseButton1Up.connect(cancelStep);

        for i in range(len(self.points)):
            z = i;
            point = self.points[i];

            btn = EmptyButton();
            btn.backgroundColor = Color4(1, 0, 0);
            btn.size = Udim2.fromOffset(150, 150);
            btn.position = Udim2.fromOffset(point.x, point.y);
            btn.parent = self.parent;
            btn.onHoverEnter.connect(lambda _: print("h"))
            firstDown = btn.onMouseButton1Down.connect(lambda _: startPointListening(btn, z));
            

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
        curve = BSpline.Curve()

        # Set up the curve
        curve.degree = len(self.points) - 1;
        curve.ctrlpts = [[v.x, v.y] for v in self.points];

        # Auto-generate knot vector
        curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

        # Set evaluation delta
        curve.delta = 0.001

        # Evaluate curve

        points: list[Vector2] = curve.evalpts;

        finalPoints: list[list[tuple[float, float]]] = []

        pointIndex = 0;
        for point in points:
            if pointIndex == len(points) - 1: continue;

            #pygame.draw.line(surf, (0, 255, 255), point, points[pointIndex + 1], 15)
            res = self.drawLineAA(pygame.Vector2(point), pygame.Vector2(points[pointIndex + 1]));
            finalPoints.append(res);

            pointIndex += 1;

        self.partitions = finalPoints;

    def render(self, dt: float):
        screen = RenderService.renderer.screen;

        surf = pygame.Surface((1280, 720));

        for point in self.partitions:
            (UL, UR, BR, BL) = point;
            pygame.gfxdraw.aapolygon(surf, (UL, UR, BR, BL), self.color.toRGBATuple())
            pygame.gfxdraw.filled_polygon(surf, (UL, UR, BR, BL), self.color.toRGBATuple())

        screen.blit(surf, (0, 0));