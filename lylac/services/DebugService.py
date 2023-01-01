from pygame import Vector2

from lylac.modules.color4 import Color4

class Point():
    vertex: Vector2;
    color: Color4;
    static: bool;

    def __init__(self, vertex: Vector2, color: Color4 = Color4(1, 0, 0), static: bool = False) -> None:
        self.vertex = vertex;
        self.color = color;
        self.static = static;
    
    def remove(self):
        if self in DebugService.points:
            DebugService.points.remove(self);

class DebugService:

    points: list[Point] = [];
    
    @staticmethod
    def plotPoint(point: Vector2, color: Color4 = Color4(1, 0, 0), static: bool = False):
        o = Point(point, color, static);
        DebugService.points.append(o);
        return o;