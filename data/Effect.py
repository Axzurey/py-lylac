from __future__ import annotations;
import time

from typing import TYPE_CHECKING

from pygame import Vector2 #stupid bypass because python hates the sanity of people
if TYPE_CHECKING:
    from data.Enemy import Enemy
    from data.tower import Tower

import lylac


class Effect:
    
    adornee: Enemy | Tower;
    level: int;
    length: float;
    timeStarted: float;
    statusIcon: lylac.Sprite | None = None;

    def __init__(self, adornee: Enemy | Tower, level: int, length: float) -> None:
        self.adornee = adornee;
        self.level = level;
        self.length = length;

        self.timeStarted = time.time();

    def trigger(self, dt: float): ...;

class Vulnerable(Effect):

    adornee: Enemy;

    def __init__(self, adornee: Enemy, level: int, length: float) -> None:
        super().__init__(adornee, level, length);

        statusIcon = lylac.Sprite();
        statusIcon.imagePath = "assets/towers/marionette-stick1.png";
        statusIcon.parent = adornee.enemyObject;
        statusIcon.size = lylac.Udim2.fromOffset(50, 50);
        statusIcon.position = lylac.Udim2.fromScale(.5, .5);
        statusIcon.anchorPoint = Vector2(.5, .5);
        statusIcon.zIndex = 98;