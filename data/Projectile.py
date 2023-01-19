from typing import TypeVar, Generic
from pygame import Vector2
import lylac;

T = TypeVar("T", lylac.GuiObject, lylac.Sprite);

class Projectile(Generic[T]):
    tether: T;

    position: Vector2;
    velocity: Vector2;
    acceleration: Vector2;

    def __init__(self, tether: T, originPosition: Vector2) -> None:
        self.tether = tether;
        self.position = originPosition;
        self.velocity = Vector2();
        self.acceleration = Vector2();

    def applyImpulse(self, impulse: Vector2):
        self.acceleration += impulse;

    def update(self, dt: float):
        self.velocity += self.acceleration * dt;
        self.position += self.velocity;
        self.acceleration = Vector2();

        self.tether.position = lylac.Udim2.fromVector2(self.position);