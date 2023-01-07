import math
from typing import Iterator, TypeVar


number = TypeVar("number", int, float);

def lerp(a: number, b: number, t: number) -> number:
    return (1 - t) * a + t * b;

def clamp(Min: number, Max: number, t: number) -> number:
    if t > Max: return Max;
    if t < Min: return Min;
    return t;

def clampAll(minV: number, maxV: number, *nums: number) -> list[number]:
    return [clamp(minV, maxV, val) for val in nums];

def denormalize(a: number, b: number, x: number) -> number:
    return x * (b - a) + a;

def normalize(a: number, b: number, x: number) -> float:
    return (x - a) / (b - a);

def pointsOnCircle(detail: int, radius: int = 1) -> Iterator[tuple[float, float]]:
    d = 360 / detail;

    for i in range(detail):
        theta = math.radians(d * i);
        x = math.cos(theta) * radius;
        y = math.sin(theta) * radius;

        yield (x, y);