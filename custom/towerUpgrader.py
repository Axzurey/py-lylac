import pygame
from custom.WorldClock import WorldClock
from data.tower import Tower
import lylac


class TowerUpgrader:

    isOpen: bool = False;
    frame: lylac.Frame;

    def __init__(self, backdrop: lylac.Sprite, tower: Tower) -> None:
        WorldClock.SET_TIMESTEP(.1);

        clickBlock = lylac.Frame();
        clickBlock.position = lylac.Udim2();
        clickBlock.size = lylac.Udim2.fromScale(1, 1);
        clickBlock.borderColor = lylac.Color4.invisible();
        clickBlock.dropShadowColor = lylac.Color4.invisible();
        clickBlock.backgroundColor = lylac.Color4.fromAlpha(.4);
        clickBlock.zIndex = 9999;

        overflowsX = tower.position.x + 550 + 50 > backdrop.absoluteSize.x;
        overflowsY = tower.position.y + 330 + 50 > backdrop.absoluteSize.y;

        recalculatedX = backdrop.absoluteSize.x - 550 - 50;
        recalculatedY = backdrop.absoluteSize.y - 330 - 50;

        f = lylac.Frame();
        f.size = lylac.Udim2.fromOffset(550, 330);
        f.anchorPoint = pygame.Vector2();
        f.position = lylac.Udim2.fromOffset(
            recalculatedX if overflowsX else tower.position.x,
            recalculatedY if overflowsY else tower.position.y);
        f.backgroundColor = lylac.Color4(.2, .2, .4);
        f.borderColor = lylac.Color4(1, 0, 0, .5);
        f.cornerRadius = 20;
        f.parent = clickBlock;

        nameLabel = lylac.TextObject();
        nameLabel.text = tower.name;
        nameLabel.textAlignX = "center";
        nameLabel.textAlignY = "center";
        nameLabel.textColor = lylac.Color4(0, 1, 1);
        nameLabel.backgroundColor = lylac.Color4(.2, .2, .4);
        nameLabel.dropShadowColor = lylac.Color4.invisible();
        nameLabel.borderColor = lylac.Color4(1, 0, 0, .5);
        nameLabel.textSize = 30;
        nameLabel.size = lylac.Udim2(0, 1, 50, 0);
        nameLabel.position = lylac.Udim2(0, .5, 25, 0)
        nameLabel.anchorPoint = pygame.Vector2(.5, .5);
        nameLabel.cornerRadius = 0;
        nameLabel.parent = f;

        descriptionBox = lylac.TextObject();
        descriptionBox.text = tower.description;
        descriptionBox.textAlignX = "left";
        descriptionBox.textAlignY = "top";
        descriptionBox.textColor = lylac.Color4();
        descriptionBox.backgroundColor = lylac.Color4.invisible();
        descriptionBox.dropShadowColor = lylac.Color4.invisible();
        descriptionBox.borderColor = lylac.Color4.invisible();
        descriptionBox.textSize = 24;
        descriptionBox.size = lylac.Udim2.fromScale(1, .1);
        descriptionBox.position = lylac.Udim2(0, .5, 85, 0);
        descriptionBox.anchorPoint = pygame.Vector2(.5, .5);
        descriptionBox.parent = f;

        destroyButton = lylac.TextButton();
        destroyButton.text = "Remove Tower";
        destroyButton.textColor = lylac.Color4();
        destroyButton.backgroundColor = lylac.Color4(.8, .1, .1);
        destroyButton.borderColor = lylac.Color4(.4, 0, 0);
        destroyButton.textSize = 24;
        destroyButton.textAlignX = "center";
        destroyButton.textAlignY = "center";
        destroyButton.position = lylac.Udim2.fromScale(.5, .85);
        destroyButton.size = lylac.Udim2.fromOffset(250, 75);
        destroyButton.anchorPoint = pygame.Vector2(.5, .5);
        destroyButton.parent = f;

        cancelButton = lylac.TextButton();
        cancelButton.text = "X";
        cancelButton.textSize = 28;
        cancelButton.backgroundColor = lylac.Color4(.8, .8, .8);
        cancelButton.textColor = lylac.Color4(1, 0, 0);
        cancelButton.textAlignX = "center";
        cancelButton.textAlignY = "center";
        cancelButton.size = lylac.Udim2.fromOffset(50, 50);
        cancelButton.anchorPoint = pygame.Vector2(.5, .5);
        cancelButton.position = lylac.Udim2.fromScale(1, 0);
        cancelButton.parent = f;

        destroyButton.onMouseButton1Down.connect(lambda _: self.destroyTower(tower));

        self.frame = clickBlock;

        clickBlock.parent = backdrop;

        clickBlock.onMouseButton1Down.connect(lambda _: self.drop());
        cancelButton.onMouseButton1Down.connect(lambda _: self.drop());

    def destroyTower(self, tower: Tower):
        from data.tower import TowerManager
        TowerManager.removeTower(tower);
        self.drop();

    def drop(self):
        from data.tower import TowerManager
        TowerManager.editorOpen = False;
        self.frame.destroy();

        WorldClock.SET_TIMESTEP(1);