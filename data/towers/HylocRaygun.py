import math
import time
import pygame
from custom.WorldClock import WorldClock
from data.Effect import Burning
from data.Enemy import EnemyManager
from data.tower import Tower
import lylac
from lylac.services.RenderService import RenderService

class HylocRaygun(Tower):
    tickDamage: float = 50 / 60; #damage / 60
    fireRate: float = 1000;
    radius: int = 200;
    ray: lylac.Sprite | None = None;
    lastFired: float = 0;

    baseCost = 200;

    name = "Hyloc™ Raygun";
    description = "A raygun made by a certain company.\nFires a ray. Ray damages enemies. Need i say more?";

    maxUpgradeLevel = 4;
    upgradePerks = [
        "Increased Tick damage",
        "Increased target radius",
        "Enemies hit by the raygun will be inflicted with 1 stack of [burning] that lasts for 2 seconds",
        "Enemies hit by the raygun will be inflicted with 2 stacks of [burning] that last for 1.5 seconds each"
    ];
    upgradeCosts = [
        150,
        200,
        300,
        400
    ];


    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "hyloc raygun tower";
        towerObject.size = lylac.Udim2.fromOffset(75, 75);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/hyloc raygun-01.png";
        towerObject.canHover = True;
        towerObject.zIndex = 90;

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;

    frame = 0;

    def createRayObject(self):
        p = lylac.Sprite();

        self.ray = p;

        p.size = lylac.Udim2.fromOffset(800, 40);
        p.imagePath = "assets/ui/lazer.png"
        p.position = lylac.Udim2.fromOffset(self.position.x, self.position.y);
        p.anchorPoint = pygame.Vector2(.5, .5);
        p.zIndex = 50;
        p.parent = self.screen;

        return p;
    
    def destroyRayObject(self):
        if self.ray:
            self.ray.destroy();
            self.ray = None;

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

        for enemy in EnemyManager.enemies:
            enemyP = enemy.enemyObject.absolutePosition;
            enemyS = enemy.enemyObject.absoluteSize;

            corners = [
                enemyP, #top left
                enemyP + pygame.Vector2(enemyS.x, 0), #top right
                enemyP + enemyS, #bottom right
                enemyP + pygame.Vector2(0, enemyS.y), #bottom, left
                enemyP + enemyS / 2 #center
            ]

            for corner in corners:
                if ray.isPointInBounding(corner):
                    enemy.takeDamage(self.tickDamage);
                    if self.upgradeLevel == 3:
                        enemy.afflictStatus(Burning(enemy, 3, 2));
                    elif self.upgradeLevel == 4:
                        enemy.afflictStatus(Burning(enemy, 3, 1.5));
                        enemy.afflictStatus(Burning(enemy, 3, 1.5));

    def update(self, dt: float):
        self.tickDamage = (100 / 60) if self.upgradeLevel > 1 else 50 / 60;
        self.radius = 250 if self.upgradeLevel >= 2 else 200;
        if time.time() - self.lastFired > 1 / (self.fireRate * WorldClock.timeStep):
            self.targetEnemy();

        super().update(dt);

    def destroy(self):
        self.destroyRayObject();
        super().destroy();