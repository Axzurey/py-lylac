import pygame
from data.tower import Tower
import lylac

class StarBlue(Tower):
    damage: float;
    fireRate: float;
    radius: int;

    def __init__(self, screen: lylac.Instance, position: pygame.Vector2) -> None:

        towerObject = lylac.Sprite();
        towerObject.name = "star-blue-tower";
        towerObject.size = lylac.Udim2.fromOffset(75, 75);
        towerObject.anchorPoint = pygame.Vector2(.5, .5);
        towerObject.position = lylac.Udim2.fromOffset(position.x, position.y);
        towerObject.imagePath = "assets/towers/star-blue.png";

        super().__init__(screen, position);

        towerObject.parent = self.screen;
        
        self.towerObject = towerObject;

    def update(self):...
