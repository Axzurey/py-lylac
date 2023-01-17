from __future__ import annotations;

from pygame import Vector2

from lylac.modules.mathf import lerp

class Udim2:
    xScale: float = 0
    yScale: float = 0
    xOffset: float = 0
    yOffset: float = 0

    def __repr__(self) -> str:
        return f"Udim2[{','.join([str(round(self.xOffset, 2)), str(round(self.xScale, 2)), str(round(self.yOffset, 2)), str(round(self.yScale, 2))])}]";

    def __eq__(self, other: Udim2):
        return self.xScale == other.xScale and self.yScale == other.yScale and self.xOffset == other.xOffset and self.yOffset == other.yOffset;

    def __init__(self, xOffset: float = 0, xScale: float = 0, yOffset: float = 0, yScale: float = 0):
        self.xOffset = xOffset
        self.xScale = xScale
        self.yOffset = yOffset
        self.yScale = yScale

    @staticmethod
    def fromVector2(vec2: Vector2):
        return Udim2(vec2.x, 0, vec2.y, 0);

    @staticmethod
    def fromVector2Scale(vec2: Vector2):
        return Udim2(0, vec2.x, 0, vec2.y);

    @staticmethod
    def fromScale(xScale: float = 0, yScale: float = 0):
        return Udim2(0, xScale, 0, yScale)

    @staticmethod
    def fromOffset(xOffset: float = 0, yOffset: float = 0):
        return Udim2(xOffset, 0, yOffset, 0)

    def toScale(self):
        return Vector2(self.xScale, self.yScale)

    def toOffset(self):
        return Vector2(self.xOffset, self.yOffset)

    def lerp(self, other: Udim2, t: float):
        return Udim2(
            lerp(self.xOffset, other.xOffset, t),
            lerp(self.xScale, other.xScale, t),
            lerp(self.yOffset, other.yOffset, t),
            lerp(self.yScale, other.yScale, t)
        )

