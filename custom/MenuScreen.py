import time
from pygame import Vector2
import lylac

CREDITS_TEXT = """
Welcome to Blue Cradle!

Credits:

> Sanity Sparer: google™
> Code: Me
> Assets: Me
> Suffering: Me
The credits end here."""

class MenuScreen:

    frame: lylac.Instance;

    onMenuExit = lylac.LylacSignal();

    aStates: list[lylac.ActionStateReturnValue];

    def __init__(self, display: lylac.Renderer) -> None:

        self.aStates = [];
        
        f = lylac.Frame();
        f.size = lylac.Udim2.fromScale(1, 1);
        f.position = lylac.Udim2();
        f.cornerRadius = 0;
        f.backgroundColor = lylac.Color4.fromRGB(195, 177, 225);
        
        playButton = lylac.TextButton();
        playButton.text = "PLAY";
        playButton.textAlignX = "center";
        playButton.textAlignY = "center";
        playButton.size = lylac.Udim2.fromOffset(400, 150);
        playButton.position = lylac.Udim2.fromScale(.5, .5);
        playButton.anchorPoint = Vector2(.5, .5);
        playButton.backgroundColor = lylac.Color4.fromRGB(167, 199, 231);
        playButton.textColor = lylac.Color4.fromRGB(15, 15, 255);
        playButton.borderColor = lylac.Color4.fromRGB(15, 50, 15);
        playButton.textSize = 40;
        playButton.cornerRadius = 20;
        playButton.parent = f;

        creditsButton = lylac.TextButton();
        creditsButton.text = "CREDITS";
        creditsButton.textAlignX = "center";
        creditsButton.textAlignY = "center";
        creditsButton.size = lylac.Udim2.fromOffset(200, 75);
        creditsButton.position = lylac.Udim2.fromScale(.5, .65);
        creditsButton.anchorPoint = Vector2(.5, .5);
        creditsButton.backgroundColor = lylac.Color4.fromRGB(255, 105, 97);
        creditsButton.textColor = lylac.Color4.fromRGB(15, 15, 255);
        creditsButton.borderColor = lylac.Color4.fromRGB(50, 15, 15);
        creditsButton.textSize = 30;
        creditsButton.cornerRadius = 15;
        creditsButton.parent = f;

        creditsFrame = lylac.Frame();
        creditsFrame.position = lylac.Udim2();
        creditsFrame.cornerRadius = 0;
        creditsFrame.size = lylac.Udim2.fromScale(1, 1);
        creditsFrame.backgroundColor = lylac.Color4.fromRGB(195, 177, 225);

        creditsHeader = lylac.TextObject();
        creditsHeader.backgroundColor = lylac.Color4.invisible();
        creditsHeader.borderColor = lylac.Color4.invisible();
        creditsHeader.dropShadowColor = lylac.Color4.invisible();
        creditsHeader.anchorPoint = Vector2(.5, .5);
        creditsHeader.textSize = 40;
        creditsHeader.text = "Credits Section™";
        creditsHeader.textAlignX = "center";
        creditsHeader.textAlignY = "center";
        creditsHeader.position = lylac.Udim2(0, .5, 45, 0);
        creditsHeader.size = lylac.Udim2.fromScale(.5, .15);
        creditsHeader.textColor = lylac.Color4.fromRGB(29, 28, 26);
        creditsHeader.textFont = "rubik"
        creditsHeader.parent = creditsFrame;

        creditsBackButton = lylac.TextButton();
        creditsBackButton.backgroundColor = lylac.Color4.fromRGB(255, 105, 97);
        creditsBackButton.text = "<";
        creditsBackButton.textColor = lylac.Color4.fromRGB(15, 15, 255);
        creditsBackButton.anchorPoint = Vector2(.5, .5);
        creditsBackButton.borderColor = lylac.Color4.fromRGB(50, 15, 15);
        creditsBackButton.position = lylac.Udim2.fromOffset(45, 45);
        creditsBackButton.size = lylac.Udim2.fromOffset(50, 50);
        creditsBackButton.cornerRadius = 35;
        creditsBackButton.textAlignX = "center";
        creditsBackButton.textAlignY = "center";
        creditsBackButton.textSize = 30;
        creditsBackButton.dropShadowColor = lylac.Color4.invisible();
        creditsBackButton.parent = creditsFrame;

        creditsText = lylac.TextObject();
        creditsText.backgroundColor = lylac.Color4.invisible();
        creditsText.borderColor = lylac.Color4.invisible();
        creditsText.dropShadowColor = lylac.Color4.invisible();
        creditsText.textColor = lylac.Color4();
        creditsText.anchorPoint = Vector2(.5, .5);
        creditsText.textSize = 25;
        creditsText.textAlignX = "center";
        creditsText.textAlignY = "center";
        creditsText.size = lylac.Udim2.fromScale(.8, .3);
        creditsText.position = lylac.Udim2.fromScale(.5, .3);
        creditsText.text = CREDITS_TEXT;
        creditsText.parent = creditsFrame;

        def toggleFrames():
            if f.parent:
                creditsFrame.parent = display;
                f.parent = None;
            else:
                f.parent = display
                creditsFrame.parent = None;

        playButtonActionState = lylac.useActionState(playButton,
            defaultProperties = {
                "backgroundColor": lylac.Color4.fromRGB(167, 199, 231),
                "rotation": 0,
                "size": lylac.Udim2.fromOffset(400, 150),
                "textSize": 40
            },
            hoverProperties = {
                "backgroundColor": lylac.Color4.fromRGB(167, 209, 241),
                "rotation": 2,
                "size": lylac.Udim2.fromOffset(410, 160),
                "textSize": 42
            }
        );

        creditsBackButtonActionState = lylac.useActionState(creditsBackButton, 
            defaultProperties = {
                "backgroundColor": lylac.Color4.fromRGB(255, 105, 97),
                "rotation": 0,
                "size": lylac.Udim2.fromOffset(50, 50),
                "textSize": 30
            },
            hoverProperties = {
                "backgroundColor": lylac.Color4.fromRGB(255, 95, 87),
                "rotation": 2,
                "size": lylac.Udim2.fromOffset(60, 60),
                "textSize": 32
            }
        )

        creditsButtonActionState = lylac.useActionState(creditsButton, 
            defaultProperties = {
                "backgroundColor": lylac.Color4.fromRGB(255, 105, 97),
                "rotation": 0,
                "size": lylac.Udim2.fromOffset(200, 75),
                "textSize": 30
            },
            hoverProperties = {
                "backgroundColor": lylac.Color4.fromRGB(255, 95, 87),
                "rotation": 2,
                "size": lylac.Udim2.fromOffset(210, 85),
                "textSize": 32
            }
        )

        playButton.onMouseButton1Up.connect(lambda _: self.drop());
        creditsBackButton.onMouseButton1Up.connect(lambda _: toggleFrames());
        creditsButton.onMouseButton1Up.connect(lambda _: toggleFrames());

        f.parent = display;
        self.frame = f;

        self.aStates.extend([playButtonActionState, creditsButtonActionState, creditsBackButtonActionState]);

    def drop(self):
        for state in self.aStates:
            state["disconnect"]();
        self.onMenuExit.dispatch();
        time.sleep(.25)
        self.frame.destroy();