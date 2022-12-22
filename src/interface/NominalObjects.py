from typing import Any
from pygame import Vector2
import pygame

from modules.lylacSignal import LylacSignal

def Corner(DX: float, DY: float, R: float):
    return DX < 0 and DY < 0 and DX * DX + DY * DY > R * R

def isPointInCircle(point: Vector2, circleOrigin: Vector2, circleRadius: float):
    return (point - circleOrigin).magnitude() < circleRadius;

def isPointInBounding(pos: Vector2, size: Vector2, point: Vector2, cornerRadius: float):
    #TODO
    bottomR = pos + size - Vector2(cornerRadius, cornerRadius);
    bottomL = pos + Vector2(0, size.y) + Vector2(cornerRadius, -cornerRadius);
    topR = pos + Vector2(size.x, 0) + Vector2(-cornerRadius, cornerRadius);
    topL = pos + Vector2(cornerRadius, cornerRadius);

    if point.x > (pos + size).x or point.y > (pos + size).y: return False;
    if point.x < (pos + size).x or point.y < (pos + size).y: return False;

    if point.x > bottomR.x and point.y > bottomR.y:
        return isPointInCircle(point, bottomR, cornerRadius);
    elif point.x > topR.x and point.y < topR.y:
        return isPointInCircle(point, topR, cornerRadius);
    elif point.x < bottomL.x and point.y > bottomL.y:
        return isPointInCircle(point, bottomL, cornerRadius);
    elif point.x < topL.x and point.y < topL.y:
        return isPointInCircle(point, bottomL, cornerRadius);


class HasBounding:
    def isPointInBounding(self: Any, point: Vector2):
        """
        The best explanation I could find. I couldn't find a single one telling me *why* this works or what it even does.
        https://stackoverflow.com/questions/71318946/round-rectangle-in-rectangle-how-to-detect-coordinates-in-corners-that-are-out
        
        
        """

        return isPointInBounding(self.absolutePosition, self.absoluteSize, point, self.cornerRadius)

        X, Y = point.xy;
        
        rect: pygame.Rect = self.boundingRect;

        Left = self.absolutePosition.x;
        Top = self.absolutePosition.y;

        Hgt = self.absoluteSize.y;
        Wdt = self.absoluteSize.x;

        R = self.cornerRadius

        Outside = (X < Left) or (X > Left + Wdt) or (Y < Top) or (Y > Top + Hgt) or Corner(X - Left - R - X, Y - Top - R, R) or Corner(X - Left - R, Top  + Hgt - R - Y, R) or Corner(Left + Wdt - R - X, Top  + Hgt - R - Y, R) or Corner(Left + Wdt - R - X, Y - Top - R, R)

        return not Outside;

class Hoverable(HasBounding):
    onHoverEnter: LylacSignal;
    onHoverExit: LylacSignal;

    _isHover: bool = False;

    def __init__(self) -> None:
        super().__init__();

        self.onHoverEnter = LylacSignal();
        self.onHoverExit = LylacSignal();

class Clickable(HasBounding):
    onMouseButton1Down: LylacSignal[None];
    onMouseButton1Up: LylacSignal[None];

    _isMouse1Down: bool = False;
    _isMouse2Down: bool = False;
    
    def __init__(self) -> None:
        super().__init__();
        
        self.onMouseButton1Down = LylacSignal[None]();
        self.onMouseButton1Up = LylacSignal[None]();