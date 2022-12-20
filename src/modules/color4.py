def clamp(x: int, minV: int, maxV: int):
    return x < minV and minV or x > maxV and maxV or x;

def clampAll(minV: int, maxV: int, *nums: int):
    return (clamp(val, minV, maxV) for val in nums)

class Color4:

    r: float;
    g: float;
    b: float;
    a: float;

    def __init__(self, r: float = 0, g: float = 0, b: float = 0, a: float = 1) -> None:
        self.r = r;
        self.g = g;
        self.b = b;
        self.a = a;

    @staticmethod
    def fromRGBA(r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        (r, g, b, a) = clampAll(0, 255, r, g, b, a);
        return Color4(r / 255, g / 255, b / 255, a / 255);
    
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