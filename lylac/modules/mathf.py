from typing import TypeVar


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