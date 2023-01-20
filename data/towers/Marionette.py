import math
import time
import pygame
from custom.WorldClock import WorldClock
from data.Effect import Vulnerable
from data.Enemy import EnemyManager
from data.Projectile import Projectile
from data.tower import Tower
import lylac
from lylac.services.RenderService import RenderService

class Marionette(Tower):
    
    name = "Marionette";
    description = "A certain song inspired me to make this. \nThis tower inflicts 1 stack of vulnerability on any enemies in the radius periodically."

    radius: int = 400;
    lastTriggered: float = 0;
    fireRate: float = .0000000000001; #1 / fireRate is the time it takes between triggers

    maxUpgradeLevel = 4;
    upgradePerks = [
        "Increased control radius",
        "Increased control radius",
        "Longer control time",
        "Increased [vulnerable] damage bonus"
    ];
    upgradeCosts = [
        125,
        200,
        300,
        375
    ];

    trackers: list[Projectile[lylac.Sprite]] = [];

    baseCost = 150;

    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "marionette-tower";
        towerObject.size = lylac.Udim2.fromOffset(75, 75);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/marionette-pixel.png";
        towerObject.zIndex = 90;
        towerObject.canHover = True;

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;
        
        for _ in range(2):
            self.createMissile();

    def createMissile(self):

        self.lastTriggered = time.time();

        projectileSprite = lylac.Sprite();
        projectileSprite.imagePath = "assets/towers/tracker.png";
        projectileSprite.size = lylac.Udim2.fromOffset(75, 75);
        projectileSprite.position = lylac.Udim2.fromVector2(self.position);
        projectileSprite.zIndex = 99;
        projectileSprite.anchorPoint = pygame.Vector2(.5, .5);
        projectileSprite.parent = self.screen;
        projectileSprite.name = str(self.lastTriggered);

        proj = Projectile(projectileSprite, self.position);

        proj.internal['lastDamage'] = 0;

        self.trackers.append(proj);

    def destroy(self):
        for proj in self.trackers:
            proj.tether.destroy();
        self.trackers = [];
        return super().destroy()

    def update(self, dt: float):

        self.radius = 400 + lylac.clamp(0, 100, self.upgradeLevel * 50);

        if time.time() - self.lastTriggered > 1 / (self.fireRate * WorldClock.timeStep):
            self.createMissile();

        target = EnemyManager.getEnemyClosestToGoalAndInRadius(self.position, self.radius ** 2);

        removingProjectiles = [];

        for proj in self.trackers:
            if target and time.time() - proj.internal['lastDamage'] > 1:
                directionToEnemy = (target.position - proj.position).normalize();
                distanceFromEnemy = (target.position - proj.position).magnitude();

                proj.tether.rotation = int(lylac.lerp(proj.tether.rotation, math.degrees(math.atan2(directionToEnemy.y, directionToEnemy.x)) + 90, .1));

                for enemy in EnemyManager.enemies:
                    dfE = (enemy.position - proj.position).magnitude();
                    if dfE <= 10:
                    #create some cool explosion!
                        enemy.takeDamage(75);
                        proj.internal['lastDamage'] = time.time();
                if distanceFromEnemy <= 40:
                    proj.applyImpulse(directionToEnemy * 5000);
                else:
                    proj.setVelocity(proj.velocity.lerp(directionToEnemy * 250, .1));

            proj.update(dt);

        self.trackers = list(filter(lambda p: p not in removingProjectiles, self.trackers));

        for proj in removingProjectiles:
            proj.tether.destroy();

        super().update(dt);