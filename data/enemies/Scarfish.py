import math
import time
import pygame
from data.Enemy import Enemy, EnemyManager
import lylac


class Scarfish(Enemy):
    speed: float = 50;
    health: float = 200;
    entropyGainedOnKill = 10;

    def __init__(self, screen: lylac.Instance) -> None:
        enemyObject = lylac.Sprite();
        enemyObject.name = "scarfish-enemy";
        enemyObject.size = lylac.Udim2.fromOffset(90, 90);
        enemyObject.anchorPoint = pygame.Vector2(.5, .5);
        enemyObject.imagePath = "assets/hazes/scarfish.png";

        super().__init__(screen);

        enemyObject.position = lylac.Udim2.fromOffset(self.position.x, self.position.y);
        enemyObject.parent = self.screen;
        
        self.enemyObject = enemyObject;

    def update(self, dt: float):
        super().update(dt);

        alpha0 = lylac.clamp(0, 1, self.alphaAlongPath);
        alpha1 = lylac.clamp(0, 1, self.alphaAlongPath + 0.005);

        a0 = EnemyManager.curve.getDeltaAlongLine(alpha0);
        a1 = EnemyManager.curve.getDeltaAlongLine(alpha1);

        if a0 and a1:
            
            d = (a1 - a0).normalize();

            rot = round(math.degrees(math.atan2(d.y, d.x))) + 90;

            self.enemyObject.rotation = rot + round(math.sin(time.time() * 25) * 15);