from __future__ import annotations
import time;
from typing import Type, TypedDict
import pygame
from data.Effect import Effect
import lylac
from lylac.services.RenderService import PostRender

class TowerInformation(TypedDict):
    name: str;
    cost: int;
    imagePath: str;
    radius: int;
    link: Type[Tower];
    targetSize: int;

class TowerManager:

    towers: list[Tower] = [];

    playerEntropy = 0;

    @PostRender("towermanagerUpdate")
    @staticmethod
    def update(dt: float):
        for tower in TowerManager.towers:
            tower.update(dt);

    @staticmethod
    def addTower(t: Tower):
        TowerManager.towers.append(t);

    @staticmethod
    def removeTower(t: Tower):
        if t in TowerManager.towers:
            TowerManager.towers.remove(t);

class Tower:

    towerObject: lylac.Sprite;
    screen: lylac.Instance;
    position: pygame.Vector2;

    effects: list[Effect]

    allowedPaddingInset: int = 15;
    
    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:
        self.screen = screen;
        self.position = position;
        self.effects = [];

    def update(self, dt: float):
        self.updateEffects(dt);

    def afflictStatus(self, effect: Effect):
        self.effects.append(effect);

    def updateEffects(self, dt: float):
        toRemove: list[Effect] = [];

        for effect in self.effects:
            effect.trigger(dt);
            if time.time() - effect.timeStarted >= effect.length:
                toRemove.append(effect);