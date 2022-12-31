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

class DraggablePolygonObject(Instance):
    points: list[Vector2];
    color: Color4;
    width: int;
    pointButtons: list[EmptyButton];

    partitions: list[list[tuple[float, float]]];

    connections: list[LylacConnection];

    def __init__(self, parent: Instance | Renderer | None = None) -> None:
        super().__init__();

        LoadDefaultGuiProperties("DraggablePolygonObject", self);

        self.partitions = [];
        self.pointButtons = [];
        self.connections = [];

        self.parent = parent;

        self._createButtons();

    def _createButtons(self):
        def startPointListening(btn: EmptyButton, index: int):
            def cancelStep(_):
                nonlocal c1;
                nonlocal c2;
                c1.disconnect();
                c2.disconnect();

            def updatePos(_):

                mousePos = InputService.getMousePosition();

                if mousePos != self.points[index]:
                    self.points[index] = mousePos;
                    self.points = self.points;
                
                btn.position = Udim2.fromOffset(mousePos.x - 15 / 2, mousePos.y - 15 / 2)

            c1 = RenderService.postRender.connect(updatePos);

            c2 = btn.onMouseButton1Up.connect(cancelStep);

            self.connections.extend((c1, c2));

        for i in range(len(self.points)):
            def t():
                z = i;
                point = self.points[i];

                btn = EmptyButton();
                btn.backgroundColor = Color4(1, 0, 0);
                btn.size = Udim2.fromOffset(15, 15);
                btn.position = Udim2.fromOffset(point.x, point.y);
                btn.parent = self.parent;

                btn.borderWidth = 1;
                btn.dropShadowOffset = Udim2();
                btn.dropShadowRadius = 0;
                
                firstDown = btn.onMouseButton1Down.connect(lambda _: startPointListening(btn, z));

                self.pointButtons.append(btn);
                self.connections.append(firstDown);
            t()
            
    def _destroyButtons(self):
        for connection in self.connections:
            connection.disconnect();
        for button in self.pointButtons:
            button.destroy();

    def createPoint(self, at: Vector2):
        self._destroyButtons();
        self.points.append(at);
        self._createButtons();
        self.update();

    def removeLastPoint(self):
        self._destroyButtons();
        self.points.pop();
        self._createButtons();
        self.update();

    def update(self): ...

    def render(self, dt: float):

        screen = RenderService.renderer.screen;

        size = screen.get_size();

        if self.parent and isinstance(self.parent, GuiObject):
            size = self.parent.absolutePosition.xy;
        
        surf = pygame.Surface(size, pygame.SRCALPHA, 32);
        surf.convert_alpha()

        pointIndex = 0;
        for point in self.points:
            if pointIndex == len(self.points) - 1:
                pygame.draw.line(surf, self.color.toRGBList(), point, self.points[0], int(self.width));
            else:
                pygame.draw.line(surf, self.color.toRGBList(), point, self.points[pointIndex + 1], int(self.width));
            pointIndex += 1;

        screen.blit(surf, (0, 0));