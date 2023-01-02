from __future__ import annotations
import pygame
import lylac;

class EnemyManager:
    enemies: list[Enemy] = [];
    curve: lylac.SegmentedLineObject;

    @staticmethod
    def update(dt: float):
        for enemy in EnemyManager.enemies:
            enemy.update();

    @staticmethod
    def addEnemy(e: Enemy):
        EnemyManager.enemies.append(e);

    @staticmethod
    def removeEnemy(e: Enemy):
        if e in EnemyManager.enemies:
            EnemyManager.enemies.remove(e);

    @staticmethod
    def getEnemyClosestToGoalAndInRadius(point: pygame.Vector2, radius: int):
        if len(EnemyManager.enemies) == 0: return None;
        
        selected = None;
        for enemy in EnemyManager.enemies:
            if selected is None and (enemy.position - point).magnitude() <= radius:
                selected = enemy;
            elif selected and enemy.alphaAlongPath > selected.alphaAlongPath and (enemy.position - point).magnitude() <= radius:
                selected = enemy;
        return selected;


class Enemy:
    
    enemyObject: lylac.Sprite;
    screen: lylac.Instance;
    position: pygame.Vector2;
    speed: float;
    health: float;

    alphaAlongPath: float = 0;

    def __init__(self, screen: lylac.Instance) -> None:
        self.screen = screen;
        self.position = EnemyManager.curve.getDeltaAlongLine(0); #type: ignore this should exist

    def update_position(self, position: pygame.Vector2):
        self.position = position;
        self.enemyObject.position = lylac.Udim2.fromOffset(position.x, position.y);

    def takeDamage(self, damage: float):
        self.health -= damage;
        if self.health <= 0 and self in EnemyManager.enemies:
            EnemyManager.enemies.remove(self);
            self.enemyObject.destroy();

    def update(self):
        self.alphaAlongPath += self.speed / 1000 / 60;
        pathRes = EnemyManager.curve.getDeltaAlongLine(self.alphaAlongPath);

        if pathRes:
            self.update_position(pathRes);
        else: ...
        if self.health <= 0 and self in EnemyManager.enemies:
            EnemyManager.enemies.remove(self);
            self.enemyObject.destroy();