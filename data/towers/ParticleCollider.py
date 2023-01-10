import asyncio
import math
import time
import pygame
from data.Enemy import EnemyManager
from data.tower import Tower, TowerManager
import lylac
from lylac.services.RenderService import RenderService

class ParticleCollider(Tower):

    lastActivated: float = 0;
    activationCooldown: float = 5;
    baseEntropyGained = 20;

    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "particle-collider-tower";
        towerObject.size = lylac.Udim2.fromOffset(75, 75);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/particle collider-01.png";
        towerObject.zIndex = 90;

        above = lylac.Sprite();
        above.name = "particle-collider-tip";
        above.size = lylac.Udim2.fromScale(1, 1);
        above.anchorPoint = pygame.Vector2(.5, .5);
        above.position = lylac.Udim2.fromScale(.5, .5);
        above.imagePath = "assets/towers/particle collider-tip-01.png"
        above.parent = towerObject;

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;

    def update(self, dt: float):
        if time.time() - self.lastActivated >= self.activationCooldown:
            TowerManager.addEntropy(self.baseEntropyGained);
            self.lastActivated = time.time();
        
        for child in self.towerObject.children:
            if child.name == "particle-collider-tip":
                child.rotation += 2;

        super().update(dt);