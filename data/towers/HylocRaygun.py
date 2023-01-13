import math
import time
import pygame
from data.Enemy import EnemyManager
from data.tower import Tower
import lylac
from lylac.services.RenderService import RenderService

class HylocRaygun(Tower):
    damage: float = 20;
    fireRate: float = 1000;
    radius: int = 200;
    ray: lylac.Sprite | None = None;
    lastFired: float = 0;

    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "hyloc raygun tower";
        towerObject.size = lylac.Udim2.fromOffset(75, 75);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/hyloc raygun-01.png";
        towerObject.zIndex = 90;

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;

    frame = 0;

    def createRayObject(self):
        p = lylac.Sprite();

        self.ray = p;

        p.size = lylac.Udim2.fromOffset(800, 100);
        p.imagePath = "assets/ui/lazer.png"
        p.backgroundColor = lylac.Color4.fromRGB(0, 255, 255);
        p.borderWidth = 0;
        p.dropShadowColor = lylac.Color4.fromAlpha(0);
        p.position = lylac.Udim2.fromOffset(self.position.x, self.position.y);
        p.anchorPoint = pygame.Vector2(.5, .5);
        p.zIndex = 50;
        p.parent = self.screen;

        return p;
    
    def destroyRayObject(self):
        if self.ray:
            self.ray.destroy();

    def targetEnemy(self):
        target = EnemyManager.getEnemyClosestToGoalAndInRadius(self.position, self.radius);

        if not target:
            return self.destroyRayObject();

        self.lastFired = time.time();

        directionToEnemy = target.position - self.position;
        unitToEnemy = directionToEnemy.normalize();

        rotationToEnemy = int(math.degrees(math.atan2(unitToEnemy.y, unitToEnemy.x))) + 90

        self.towerObject.rotation = rotationToEnemy;

        ray = self.ray if self.ray else self.createRayObject();

        ray.rotation = rotationToEnemy - 90;

        self.frame += .25;
        ray.imagePath = "assets/ui/lazer2.png" if round(self.frame) % 2 == 0 else "assets/ui/lazer2.png";

    def update(self, dt: float):
        if time.time() - self.lastFired > 1 / self.fireRate:
            self.targetEnemy();

        super().update(dt);