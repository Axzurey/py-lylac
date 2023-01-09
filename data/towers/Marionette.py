import asyncio
import math
import time
import pygame
from data.Effect import Vulnerable
from data.Enemy import EnemyManager
from data.tower import Tower
import lylac
from lylac.services.RenderService import RenderService

class Marionette(Tower):
    
    radius: int = 500;
    lastTriggered: float = 0;
    fireRate: float = .5; #1 / fireRate is the time it takes between triggers

    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "marionette-tower";
        towerObject.size = lylac.Udim2.fromOffset(75, 75);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/marionette-pixel.png";
        towerObject.zIndex = 90;

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;

    def targetEnemy(self):
        targets = EnemyManager.getAllEnemiesInRadius(self.position, self.radius);

        if not targets: return;

        self.lastTriggered = time.time();

        p = lylac.Frame();
        p.cornerRadius = self.radius;
        p.size = lylac.Udim2.fromOffset(10, 10);
        p.position = lylac.Udim2.fromOffset(self.position.x, self.position.y);
        p.backgroundColor = lylac.Color4(1, 0, 0, .5);
        p.dropShadowRadius = 0;
        p.dropShadowOffset = lylac.Udim2();
        p.anchorPoint = pygame.Vector2(.5, .5);
        p.borderColor = lylac.Color4.fromAlpha(0);
        p.dropShadowColor = lylac.Color4.fromAlpha(0);
        p.borderWidth = 0;
        p.parent = self.towerObject.parent;
        lylac.CleanupService.cleanUp(p, .4);

        lylac.AnimationService.createAnimation(p, "size", lylac.Udim2.fromOffset(self.radius, self.radius), .3, lylac.InterpolationMode.easeInQuint);
        
        lylac.CleanupService.delay(.3, lambda targets: [target.afflictStatus(Vulnerable(target, 5, 2)) for target in targets], targets)

    def update(self, dt: float):
        if time.time() - self.lastTriggered > 1 / self.fireRate:
            self.targetEnemy();

        super().update(dt);