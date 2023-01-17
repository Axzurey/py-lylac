import pygame
from custom.WorldClock import WorldClock
from data.tower import Tower, TowerManager
import lylac


class TowerUpgrader:

    isOpen: bool = False;
    frame: lylac.Frame;
    radiusFrame: lylac.Frame | None = None;
    conBin = lylac.useSignalBin();

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

        if hasattr(tower, 'radius'):
            radiusFrame = lylac.Frame();
            radiusFrame.size = lylac.Udim2.fromOffset(tower.radius, tower.radius); #type: ignore [hasattr proves it exists]
            radiusFrame.cornerRadius = 180;
            radiusFrame.position = lylac.Udim2.fromVector2(tower.position);
            radiusFrame.backgroundColor = lylac.Color4(0, 1, 1, .4);
            radiusFrame.borderColor = lylac.Color4.invisible();
            radiusFrame.dropShadowColor = lylac.Color4.invisible();
            radiusFrame.enabled = False;
            radiusFrame.canHover = False;
            radiusFrame.anchorPoint = pygame.Vector2(.5, .5);
            radiusFrame.parent = backdrop;
            self.radiusFrame = radiusFrame;

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
        descriptionBox.textSize = 20;
        descriptionBox.size = lylac.Udim2.fromScale(1, .1);
        descriptionBox.position = lylac.Udim2(0, .5, 85, 0);
        descriptionBox.anchorPoint = pygame.Vector2(.5, .5);
        descriptionBox.parent = f;

        upgradeButton = lylac.TextButton();
        upgradeButton.text = f"Upgrade Tower {tower.upgradeLevel}/{tower.maxUpgradeLevel}\n${tower.upgradeCosts[tower.upgradeLevel + 1]}" if tower.upgradeLevel < tower.maxUpgradeLevel else "MAX LEVEL";
        upgradeButton.textSize = 16;
        upgradeButton.textAlignX = "center";
        upgradeButton.textAlignY = "center";
        upgradeButton.textColor = lylac.Color4.fromGreen(1);
        upgradeButton.backgroundColor = lylac.Color4(.3, .3, .3);
        upgradeButton.borderColor = lylac.Color4.fromGreen(.7);
        upgradeButton.anchorPoint = pygame.Vector2(.5, .5);
        upgradeButton.position = lylac.Udim2.fromScale(.8, .85);
        upgradeButton.size = lylac.Udim2.fromOffset(200, 55);
        upgradeButton.parent = f;

        destroyButton = lylac.TextButton();
        destroyButton.text = f"Sell Tower ${tower.baseCost // 2}";
        destroyButton.textColor = lylac.Color4();
        destroyButton.backgroundColor = lylac.Color4(.8, .1, .1);
        destroyButton.borderColor = lylac.Color4(.4, 0, 0);
        destroyButton.textSize = 16;
        destroyButton.textAlignX = "center";
        destroyButton.textAlignY = "center";
        destroyButton.position = lylac.Udim2.fromScale(.2, .85);
        destroyButton.size = lylac.Udim2.fromOffset(200, 55);
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

        def update():
            if tower.upgradeLevel < tower.maxUpgradeLevel:
                if TowerManager.playerEntropy < tower.upgradeCosts[tower.upgradeLevel + 1] and upgradeButton.backgroundColor != lylac.Color4(.3, .3, .3):
                    upgradeButton.backgroundColor = lylac.Color4(.3, .3, .3);
                elif TowerManager.playerEntropy >= tower.upgradeCosts[tower.upgradeLevel + 1] and upgradeButton.backgroundColor != lylac.Color4():
                    upgradeButton.backgroundColor = lylac.Color4();

                upgText = f"Upgrade Tower {tower.upgradeLevel}/{tower.maxUpgradeLevel}\n${tower.upgradeCosts[tower.upgradeLevel + 1]}";
                if upgradeButton.text != upgText:
                    upgradeButton.text = upgText;
            elif upgradeButton.text != "MAX LEVEL":
                upgradeButton.text = "MAX LEVEL";

            sellPrice = tower.baseCost;

            for i in range(tower.upgradeLevel) :
                sellPrice += tower.upgradeCosts[i];

            sellPrice //= 2;

            targetText = f"Sell Tower ${sellPrice}";

            if destroyButton.text != targetText:
                destroyButton.text = targetText;

        def upgrade():
            if tower.upgradeLevel == tower.maxUpgradeLevel: return;
            if TowerManager.playerEntropy < tower.upgradeCosts[tower.upgradeLevel + 1]: return;

            TowerManager.addEntropy(-tower.upgradeCosts[tower.upgradeLevel + 1]);

            tower.upgradeLevel += 1;

        upgradeButton.onMouseButton1Down.connect(lambda _: upgrade());

        self.conBin.add(lylac.RenderService.postRender.connect(lambda _: update()));

        clickBlock.onMouseButton1Down.connect(lambda _: self.drop());
        cancelButton.onMouseButton1Down.connect(lambda _: self.drop());

    def destroyTower(self, tower: Tower):
        from data.tower import TowerManager
        TowerManager.removeTower(tower);

        sellPrice = tower.baseCost;

        for i in range(tower.upgradeLevel) :
            sellPrice += tower.upgradeCosts[i];

        sellPrice //= 2;

        TowerManager.addEntropy(sellPrice);

        self.drop();

    def drop(self):
        from data.tower import TowerManager
        TowerManager.editorOpen = False;
        self.frame.destroy();
        self.conBin.drop();

        if self.radiusFrame:
            self.radiusFrame.destroy();

        WorldClock.SET_TIMESTEP(1);