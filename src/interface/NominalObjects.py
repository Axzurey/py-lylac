from typing import Any
from pygame import Vector2
import pygame

def Corner(DX: float, DY: float, R: float):
    return DX < 0 and DY < 0 and DX * DX + DY * DY > R * R

class HasBounding:
    def isPointInBounding(self: Any, point: Vector2):
        """
        The best explanation I could find. I couldn't find a single one telling me *why* this works or what it even does.
        https://stackoverflow.com/questions/71318946/round-rectangle-in-rectangle-how-to-detect-coordinates-in-corners-that-are-out
        """
        X, Y = point.xy;
        
        rect: pygame.Rect = self.boundingRect;

        Left = rect.left;
        Top = rect.top;

        Hgt = rect.height;
        Wdt = rect.width;

        R = self.cornerRadius

        Outside = (X < Left) or (X > Left + Wdt) or (Y < Top) or (Y > Top + Hgt) or Corner(X - Left - R - X, Y - Top - R, R) or Corner(X - Left - R, Top  + Hgt - R - Y, R) or Corner(Left + Wdt - R - X, Top  + Hgt - R - Y, R) or Corner(Left + Wdt - R - X, Y - Top - R, R)

        return not Outside;

class Hoverable(HasBounding): ...

class Clickable(HasBounding): ...