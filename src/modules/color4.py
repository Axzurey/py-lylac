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
        return Color4(r / 255, g / 255, b / 255, a / 255);
    
    def toRGBATuple(self):
        return (self.r * 255, self.g * 255, self.b * 255, self.a * 255);
    def toRGBAList(self):
        return [self.r * 255, self.g * 255, self.b * 255, self.a * 255];
    def toTuple(self):
        return (self.r, self.g, self.b, self.a);
    def toList(self):
        return [self.r, self.g, self.b, self.a];