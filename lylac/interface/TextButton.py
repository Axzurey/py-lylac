from lylac.interface.NominalObjects import Clickable, Hoverable
from lylac.interface.TextObject import TextObject;
from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties

class TextButton(TextObject, Clickable, Hoverable):

    def __init__(self) -> None:
        TextObject.__init__(self);
        Clickable.__init__(self);
        Hoverable.__init__(self);

        LoadDefaultGuiProperties('TextButton', self);

    def update(self):
        super().update();

    def render(self, dt: float):
        super().render(dt);
        self.renderText();