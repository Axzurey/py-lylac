from __future__ import annotations;
from lylac.modules.mathf import clampAll, lerp;

class Color4:

    r: float;
    g: float;
    b: float;
    a: float;

    def __repr__(self) -> str:
        return f"Color4[{','.join([str(self.r), str(self.g), str(self.b), str(self.a)])}]";

    def __eq__(self, other: Color4):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a;

    def __init__(self, r: float = 0, g: float = 0, b: float = 0, a: float = 1) -> None:
        (r, g, b, a) = clampAll(0, 1, r, g, b, a);
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = a;

    @staticmethod
    def fromAlpha(alpha: float):
        return Color4(0, 0, 0, alpha);

    @staticmethod
    def fromRGBA(r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        (r, g, b, a) = clampAll(0, 255, r, g, b, a);
        return Color4(r / 255, g / 255, b / 255, a / 255);
    @staticmethod
    def fromRGB(r: int = 0, g: int = 0, b: int = 0):
        (r, g, b) = clampAll(0, 255, r, g, b);
        return Color4(r / 255, g / 255, b / 255, 1);
    
    def toRGBATuple(self) -> tuple[int, int, int, int]:
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255), int(self.a * 255));
    def toRGBAList(self) -> list[int]:
        return [int(self.r * 255), int(self.g * 255), int(self.b * 255), int(self.a * 255)];
    def toRGBTuple(self) -> tuple[int, int, int]:
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255));
    def toRGBList(self) -> list[int]:
        return [int(self.r * 255), int(self.g * 255), int(self.b * 255)];
    def toTuple(self):
        return (self.r, self.g, self.b, self.a);
    def toList(self):
        return [self.r, self.g, self.b, self.a];
    def lerp(self, other: Color4, t: float):
        return Color4(
            lerp(self.r, other.r, t),
            lerp(self.g, other.g, t),
            lerp(self.b, other.b, t),
            lerp(self.a, other.a, t)
        )
