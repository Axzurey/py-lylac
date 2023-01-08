from __future__ import annotations
import time
import pygame
import lylac
from lylac.services.RenderService import PostRender;
from data.Effect import Effect, Vulnerable

class EnemyManager:
    enemies: list[Enemy] = [];
    curve: lylac.SegmentedLineObject;

    enemiesEmpty = lylac.LylacSignal();

    totalEnemyCount = 0;
    emptyDispatch = 0;

    @PostRender("enemymangerUpdate")
    @staticmethod
    def update(dt: float):
        if len(EnemyManager.enemies) == 0 and EnemyManager.totalEnemyCount != EnemyManager.emptyDispatch:
            EnemyManager.enemiesEmpty.dispatch(None);
            EnemyManager.emptyDispatch = EnemyManager.totalEnemyCount;

        for enemy in EnemyManager.enemies:
            enemy.update(dt);

    @staticmethod
    def addEnemy(e: Enemy):
        EnemyManager.totalEnemyCount += 1;
        EnemyManager.enemies.append(e);

    @staticmethod
    def removeEnemy(e: Enemy):
        if e in EnemyManager.enemies:
            EnemyManager.enemies.remove(e);

    @staticmethod
    def getEnemyClosestToGoalAndInRadius(point: pygame.Vector2, radius: int) -> Enemy | None:
        if len(EnemyManager.enemies) == 0: return None;

        selected = None;
        for enemy in EnemyManager.enemies:
            if selected is None and (enemy.position - point).magnitude() <= radius:
                selected = enemy;
            elif selected and enemy.alphaAlongPath > selected.alphaAlongPath and (enemy.position - point).magnitude() <= radius:
                selected = enemy;
        return selected;

    @staticmethod
    def getAllEnemiesInRadius(point: pygame.Vector2, radius: int) -> list[Enemy] | None:
        if len(EnemyManager.enemies) == 0: return None;

        enemies = [];
        for enemy in EnemyManager.enemies:
            if (enemy.position - point).magnitude() <= radius:
                enemies.append(enemy);

        return enemies;


class Enemy:
    
    enemyObject: lylac.Sprite;
    screen: lylac.Instance;
    position: pygame.Vector2;
    speed: float;
    health: float;

    alphaAlongPath: float = 0;

    effects: list[Effect];

    def __init__(self, screen: lylac.Instance) -> None:
        self.screen = screen;
        self.position = EnemyManager.curve.getDeltaAlongLine(0); #type: ignore this should exist
        self.effects = [];

    def update_position(self, position: pygame.Vector2):
        self.position = position;
        self.enemyObject.position = lylac.Udim2.fromOffset(position.x, position.y);

    def takeDamage(self, damage: float):
        for effect in self.effects:
            if isinstance(effect, Vulnerable):
                damage += 3 ** effect.level + 15;
        self.health -= damage;
        if self.health <= 0 and self in EnemyManager.enemies:
            self.destroy();

    def destroy(self):
        EnemyManager.enemies.remove(self);
        self.enemyObject.destroy();

    def afflictStatus(self, effect: Effect):
        self.effects.append(effect);

    def updateEffects(self, dt: float):
        toRemove: list[Effect] = [];

        for effect in self.effects:
            effect.trigger(dt);
            if time.time() - effect.timeStarted >= effect.length:
                toRemove.append(effect);

        for effect in toRemove:
            if effect in self.effects:
                self.effects.remove(effect);
                if effect.statusIcon:
                    effect.statusIcon.destroy();

    def update(self, dt: float):
        self.alphaAlongPath += self.speed / 1000 * dt;

        pathRes = EnemyManager.curve.getDeltaAlongLine(self.alphaAlongPath);

        if self.alphaAlongPath >= 1:
            self.destroy();
            #TODO: this should affect the player's health counter or something

        if pathRes:
            self.update_position(pathRes);
        
        if self.health <= 0 and self in EnemyManager.enemies:
            self.destroy();

        self.updateEffects(dt);
        