from __future__ import annotations;
from typing import Type, TypedDict
import pygame
import lylac

class TowerInformation(TypedDict):
    name: str;
    cost: int;
    imagePath: str;
    radius: int;
    link: Type[Tower];
    targetSize: int;

class TowerManager:

    towers: list[Tower] = [];

    @staticmethod
    def update(dt: float):
        for tower in TowerManager.towers:
            tower.update();

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

    allowedPaddingInset: int = 15;
    
    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:
        self.screen = screen;
        self.position = position;

    def update(self): ...