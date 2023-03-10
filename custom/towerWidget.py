from pygame import Vector2
from data.tower import Tower, TowerInformation, TowerManager
import lylac
from lylac.services.InputService import InputService
from lylac.services.RenderService import RenderService

class TowerWidget:
    towerInfo: list[TowerInformation];

    widgetOpen: bool = True;

    def closeAnimation(self):
        lylac.AnimationService.createAnimation(self.frame, "position", lylac.Udim2.fromOffset(1280 / 2, (720 + 20)), .25, lylac.InterpolationMode.easeOutSine);

    def openAnimation(self):
        lylac.AnimationService.createAnimation(self.frame, "position", lylac.Udim2.fromOffset(1280 / 2, (720 - 100 / 2)), .25, lylac.InterpolationMode.easeOutSine);

    def close(self):
        self.widgetOpen = False;
        self.closeAnimation();
        self.toggleButton.text = "^";
    
    def open(self):
        self.widgetOpen = True;
        self.openAnimation();
        self.toggleButton.text = "X";

    display: lylac.Instance;
    frame: lylac.Frame;
    towerFrame: lylac.Frame;
    toggleButton: lylac.TextButton;
    openButton: lylac.TextButton;
    areaPolygons: list[lylac.PolygonObject];
    currentWorldSelectedTower: Tower | None = None;

    def checkInArea(self, point: Vector2):
        for tower in TowerManager.towers:
            if (tower.position - point).magnitude() <= tower.towerObject.size.xOffset - tower.allowedPaddingInset:
                return False;
        for poly in self.areaPolygons:
            if poly.isPointInPolygon(point):
                return True;
        return False;

    placingTower = False;
    def startTowerPlacement(self, towerIndex: int):
        self.close();
        self.placingTower = True;

        towerInfo = self.towerInfos[towerIndex];

        if TowerManager.playerEntropy < towerInfo["cost"]: return; #not enough money c:

        f = lylac.TextObject();
        f.zIndex = 10000;
        f.parent = self.frame;
        f.text = "X";
        f.textAlignX = 'center';
        f.backgroundColor = lylac.Color4(.25, 0, 0);
        f.textColor = lylac.Color4(1, 0, 0)
        f.textSize = 40;
        f.textAlignY = 'center';
        f.size = lylac.Udim2.fromScale(1, 1);

        back = lylac.Frame();
        back.backgroundColor = lylac.Color4(1, 0, 0, .5);
        back.borderColor = lylac.Color4(0, 0, 0, 0)
        back.dropShadowColor = lylac.Color4(0, 0, 0, 0)
        back.size = lylac.Udim2.fromOffset(towerInfo['radius'], towerInfo['radius']);
        back.borderWidth = 0;
        back.dropShadowRadius = 0;
        back.dropShadowOffset = lylac.Udim2()
        back.anchorPoint = Vector2(.5, .5);
        back.parent = self.display;
        back.name = "hover sprite background";
        back.cornerRadius = 9999;

        spr = lylac.Sprite();
        spr.imagePath = towerInfo["imagePath"];
        spr.size = lylac.Udim2.fromOffset(towerInfo["targetSize"] / 1.5, towerInfo["targetSize"] / 1.5);
        spr.parent = self.display;
        spr.anchorPoint = Vector2(.5, .5);
        spr.name = "hover sprite";

        def cancel():
            c0.disconnect();
            c1.disconnect();
            back.destroy();
            spr.destroy();
            f.destroy();
            self.placingTower = False;

        def place():
            tower = towerInfo["link"](self.display, InputService.getMousePosition());
            cancel();
            TowerManager.addTower(tower);
            TowerManager.addEntropy(-towerInfo["cost"]);
            self.placingTower = False;

        def updateSprPosition(_):
            mPos = InputService.getMousePosition();
            back.position = lylac.Udim2.fromOffset(mPos.x, mPos.y);
            spr.position = lylac.Udim2.fromOffset(mPos.x, mPos.y);

            if self.checkInArea(InputService.getMousePosition()):
                back.backgroundColor = lylac.Color4(0, 1, 0, .5);
            else:
                back.backgroundColor = lylac.Color4(1, 0, 0, .5);

        c0 = InputService.onMouseButton1Up.connect(
            lambda _: cancel() 
            if self.widgetOpen and self.frame.isPointInBounding(InputService.getMousePosition()) 
            else place() if self.checkInArea(InputService.getMousePosition()) else 0
        );

        c1 = RenderService.postRender.connect(updateSprPosition)


    def updateTowerDisplay(self):
        for child in self.frame.children:
            if child.name == "tower-icon":
                child.destroy();
        i = 0;
        for tower in self.towerInfos:
            def pythonPleaseScopeVariablesForLoops(): #typical python behavior
                icon = lylac.ImageButton();
                icon.imagePath = tower["imagePath"];
                icon.relativeSize = "yy";
                icon.anchorPoint = Vector2(.5, .5)
                icon.size = lylac.Udim2.fromScale(.75, .75);
                icon.name = "tower-icon";
                icon.internalStore['cost'] = tower["cost"];

                iconRed = lylac.Frame();
                iconRed.size = lylac.Udim2.fromScale(1, 1);
                iconRed.position = lylac.Udim2();
                iconRed.borderColor = lylac.Color4.invisible();
                iconRed.dropShadowColor = lylac.Color4.invisible();
                iconRed.backgroundColor = lylac.Color4(1, 0, 0, .25) if tower["cost"] < TowerManager.playerEntropy else lylac.Color4.invisible();
                iconRed.name = "redscreen";
                iconRed.canHover = True;
                iconRed.parent = icon;

                costIcon = lylac.Sprite();
                costIcon.anchorPoint = Vector2(.5, .5);
                costIcon.position = lylac.Udim2.fromScale(.8, 0);
                costIcon.size = lylac.Udim2.fromOffset(40, 40);
                costIcon.imagePath = "assets/ui/entropy_coin-01.png"
                costIcon.parent = icon;
                costIcon.zIndex = 10 + i;

                costText = lylac.TextObject();
                costText.textAlignX = "left";
                costText.textAlignY = "center";
                costText.anchorPoint = Vector2(.5, .5);
                costText.size = lylac.Udim2.fromOffset(80, 10);
                costText.text = "x" + str(tower["cost"]);
                costText.textSize = 17;
                costText.position = lylac.Udim2(40, .85, 0, 0);
                costText.backgroundColor = lylac.Color4.invisible();
                costText.borderColor = lylac.Color4.invisible();
                costText.dropShadowColor = lylac.Color4.invisible();
                costText.textColor = lylac.Color4.white();
                costText.parent = icon;
                costText.zIndex = 10 + i;

                icon.parent = self.frame;

                lylac.useActionState(iconRed, 
                    defaultProperties={"size": lylac.Udim2.fromScale(.75, .75)}, 
                    hoverProperties={"size": lylac.Udim2.fromScale(.8, .8)},
                    forInstance=icon
                )

                z = i;

                calcP = Vector2(0, self.frame.absoluteSize.y / 2) + Vector2(120, 0) * z + Vector2(50, 0);

                icon.onMouseButton1Up.connect(lambda _: self.startTowerPlacement(z));
                costIcon.onMouseButton1Up.connect(lambda _: self.startTowerPlacement(z));
                iconRed.onMouseButton1Up.connect(lambda _: self.startTowerPlacement(z));

                icon.position = lylac.Udim2(calcP.x, 0, 0, .5);

            pythonPleaseScopeVariablesForLoops();

            i += 1;

    def hide(self):
        self.frame.parent = None;
    
    def show(self):
        self.frame.parent = self.display;

    def update_icon_color_for_entropy_change(self, entropy: int):
        for child in self.frame.children:
            if child.name == "tower-icon":
                if 'cost' in child.internalStore and child.internalStore['cost'] > entropy:
                    for sub in child.children:
                        if sub.name != "redscreen": continue;
                        sub.backgroundColor = lylac.Color4(1, 0, 0, .25);
                else:
                    for sub in child.children:
                        if sub.name != "redscreen": continue;
                        sub.backgroundColor = lylac.Color4.invisible();

    def __init__(self, display: lylac.Instance, towerInfo: list[TowerInformation], areaPolygons: list[lylac.PolygonObject]) -> None:
        self.towerInfos = towerInfo;
        self.areaPolygons = areaPolygons;

        frame = lylac.Frame();
        frame.zIndex = 999;
        frame.cornerRadius = 0;
        frame.size = lylac.Udim2.fromOffset(1280, 100)
        frame.anchorPoint = Vector2(.5, .5)
        frame.position = lylac.Udim2.fromOffset(1280 / 2, (720 - 100 / 2))
        frame.borderWidth = 5;
        frame.backgroundColor = lylac.Color4.fromRGB(40, 40, 40)
        frame.borderColor = lylac.Color4.fromRGB(0, 255, 0);

        TowerManager.entropyChanged.connect(self.update_icon_color_for_entropy_change);

        frame.onHoverEnter.connect(lambda _: self.open() if not self.widgetOpen else 1);
        frame.onHoverExit.connect(lambda _: self.close() if self.widgetOpen and not frame.isPointInBounding(InputService.getMousePosition()) else 1);

        self.frame = frame;
        self.display = display;
        
        toggle = lylac.TextButton();
        toggle.zIndex = 1000;
        toggle.text = "X";
        toggle.size = lylac.Udim2.fromOffset(50, 50);
        toggle.position = lylac.Udim2.fromScale(.96, -.3);
        toggle.textColor = lylac.Color4(1, 0, 0);
        toggle.backgroundColor = lylac.Color4(.02, .02, .02);
        toggle.borderWidth = 5;
        toggle.cornerRadius = 45;
        toggle.textAlignX = 'center';
        toggle.textAlignY = 'center';
        toggle.textSize = 24;
        toggle.borderColor = lylac.Color4(1, .2, .2);
        toggle.parent = frame;

        towerFrame = lylac.Frame();
        towerFrame.size = lylac.Udim2.fromOffset(100, 200);
        towerFrame.zIndex = 100;
        towerFrame.backgroundColor = lylac.Color4.fromRGB(25, 25, 25);
        towerFrame.borderWidth = 5;
        towerFrame.cornerRadius = 15;

        self.toggleButton = toggle;

        self.updateTowerDisplay();

        toggle.onMouseButton1Up.connect(lambda _: self.close() if self.widgetOpen else self.open());