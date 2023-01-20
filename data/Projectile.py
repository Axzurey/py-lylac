from typing import Any, TypeVar, Generic
from pygame import Vector2
import lylac;

T = TypeVar("T", lylac.GuiObject, lylac.Sprite);

class Projectile(Generic[T]):
    tether: T;

    position: Vector2;
    velocity: Vector2;
    acceleration: Vector2;
    internal: dict[Any, Any];

    def __init__(self, tether: T, originPosition: Vector2) -> None:
        self.tether = tether;
        self.position = originPosition.copy();
        self.velocity = Vector2();
        self.acceleration = Vector2();
        self.internal = {};

    def applyImpulse(self, impulse: Vector2):
        self.acceleration += impulse;

    def setVelocity(self, velocity: Vector2):
        self.velocity = velocity;

    def update(self, dt: float):
        self.velocity += self.acceleration * dt;
        self.position += self.velocity * dt;
        self.acceleration = Vector2();

        self.velocity /= 1.01

        self.tether.position = lylac.Udim2.fromVector2(self.position);