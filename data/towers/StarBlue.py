import asyncio
import math
import time
import pygame
from data.Enemy import EnemyManager
from data.tower import Tower
import lylac
from lylac.services.RenderService import RenderService

class StarBlue(Tower):
    damage: float = 20;
    fireRate: float = 15;
    radius: int = 200;

    lastFired: float = 0;

    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "star-blue-tower";
        towerObject.size = lylac.Udim2.fromOffset(125, 125);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/star-blue.png";
        towerObject.zIndex = 90;

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;

    def targetEnemy(self):
        target = EnemyManager.getEnemyClosestToGoalAndInRadius(self.position, self.radius);

        if not target: return;

        self.lastFired = time.time();

        p = lylac.Frame();
        p.size = lylac.Udim2.fromOffset(10, 10);
        p.backgroundColor = lylac.Color4.fromRGB(0, 255, 255);
        p.borderWidth = 0;
        p.dropShadowColor = lylac.Color4.fromAlpha(0);
        p.position = lylac.Udim2.fromOffset(self.position.x, self.position.y);
        p.anchorPoint = pygame.Vector2(.5, .5);
        p.cornerRadius = 90;
        p.zIndex = 50;
        p.parent = self.screen;

        directionToEnemy = target.position - self.position;
        unitToEnemy = directionToEnemy.normalize();
        distanceToEnemy = directionToEnemy.magnitude();

        self.towerObject.rotation = int(math.degrees(math.atan2(unitToEnemy.y, unitToEnemy.x))) + 90;

        t = 0;

        def setPosOfProjectile(dt):

            directionToEnemy = target.position - self.position;
            unitToEnemy = directionToEnemy.normalize();
            distanceToEnemy = directionToEnemy.magnitude();

            nonlocal t;
            t = lylac.clamp(0, distanceToEnemy, t + 1500 * dt);
            tPos = self.position + unitToEnemy * t;
            p.position = lylac.Udim2.fromOffset(tPos.x, tPos.y)
            if t >= distanceToEnemy or target.health <= 0:
                nonlocal c0;
                p.destroy();
                c0.disconnect();
                target.takeDamage(self.damage);


        c0 = RenderService.postRender.connect(setPosOfProjectile);

        asyncio.run(lylac.CleanupService.cleanUp(p, 3.5, lambda: c0.disconnect()))


    def update(self):
        if time.time() - self.lastFired > 1 / self.fireRate:

            self.targetEnemy();