import pygame
from data.Enemy import Enemy, EnemyManager
import lylac


class MidnightEye(Enemy):
    speed: float = 50;
    health: float = 200;
    entropyGainedOnKill = 10;

    def __init__(self, screen: lylac.Instance) -> None:
        enemyObject = lylac.Sprite();
        enemyObject.name = "midnight-eye-enemy";
        enemyObject.size = lylac.Udim2.fromOffset(90, 90);
        enemyObject.anchorPoint = pygame.Vector2(.5, .5);
        enemyObject.imagePath = "assets/hazes/eye-of-midnightbody.png";

        eyes = lylac.Sprite();
        eyes.anchorPoint = pygame.Vector2(.5, .5);
        eyes.name = "midnight-eye-enemy-eyes";
        eyes.size = lylac.Udim2.fromScale(.5, .5);
        eyes.relativeSize = 'xx';
        eyes.position = lylac.Udim2.fromScale(.5, .5);
        eyes.imagePath = "assets/hazes/eye-of-midnighteyes.png";
        eyes.parent = enemyObject;

        super().__init__(screen);

        enemyObject.position = lylac.Udim2.fromOffset(self.position.x, self.position.y);
        enemyObject.parent = self.screen;
        
        self.enemyObject = enemyObject;

    def update(self, dt: float):
        self.enemyObject.rotation = (self.enemyObject.rotation + 5) % 360;
        return super().update(dt);