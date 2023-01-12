from __future__ import annotations
import time
from typing import Any
import lylac.client.renderer as cliRen
from lylac.modules.util import rawSet
from lylac.services.RenderService import RenderService
from lylac.modules.lylacSignal import LylacSignal;

PROPERTIES_THAT_FORCE_RERENDER = [
    "size", "parent", "position", "children", "backgroundColor", "borderColor",
    "cornerRadius", "borderWidth", "dropShadowColor", "dropShadowRadius", "dropShadowOffset",
    "text", "textColor", "textSize", "textFont", "textAlignX", "textAlignY", "enabled",
    "zIndex", "rotation", "points", "width", "color", "showControlPoints",
    "imagePath", "visible", "centerOfRotation"
];

PROPERTY_UPDATE_MAP = {
    "size": ["update", "update_image", "update_surfaces"],
    "position": ["update", "recalculate_surface_positions_for_position_change"],
    "imagePath": ["update", "update_image", "update_surfaces"],
    "rotation": ["update", "update_image", "update_surfaces"],
    "cornerRadius": ["update", "update_image", "update_surfaces"],
    "parent": ["update", "update_image", "update_surfaces"],
    "borderWidth": ["update", "update_image", "update_surfaces"],
    "borderColor": ["update", "update_image", "update_surfaces"],
    "backgroundColor": ["update", "update_image", "update_surfaces"],
    "dropShadowRadius": ["update", "update_image", "update_surfaces"],
    "dropShadowOffset": ["update", "update_image", "update_surfaces"],
    "visible": ["update", "update_image", "update_surfaces"],
    "centerOfRotation": ["update", "update_image", "update_surfaces"]
}

class Instance():
    parent: cliRen.Renderer | Instance | None = None;
    children: list[Instance];
    name: str;
    _ongoingAnimations: list[Animation];
    internalStore: dict[Any, Any];

    def __setitem__(self, key: str, value: Any):
        self.__setattr__(key, value);

    def __getitem__(self, key: str):
        return self.__getattribute__(key) or super().__getattribute__(key);

    def _updateChildrenRecursive(self, prop: str):
        for child in self.children:
            if prop in PROPERTIES_THAT_FORCE_RERENDER:
                if prop in PROPERTY_UPDATE_MAP:
                    for c in PROPERTY_UPDATE_MAP[prop]:
                        if hasattr(child.__class__, c) and callable(getattr(child.__class__, c)):
                            getattr(child.__class__, c)(child);
                    child._updateChildrenRecursive(prop);
                else:
                    child.update();
                    child._updateChildrenRecursive(prop);

    def __setattr__(self, prop: str, value: Any) -> None:
        if prop == 'parent':
            self.setParent(value);
        super().__setattr__(prop, value);
        if prop in PROPERTIES_THAT_FORCE_RERENDER:
            if prop in PROPERTY_UPDATE_MAP:
                for c in PROPERTY_UPDATE_MAP[prop]:
                    if hasattr(self.__class__, c) and callable(getattr(self.__class__, c)):
                        getattr(self.__class__, c)(self);
                self._updateChildrenRecursive(prop);
            else:
                self._updateChildrenRecursive(prop);
                self.update();

    def __getattribute__(self, prop: str):
        return super().__getattribute__(prop);
        

    def setParent(self, to: cliRen.Renderer | Instance | None):
        if to:
            if self in to.children: return;
            rawSet(self, 'parent', to);
            to.children.append(self);
        else:
            if self.parent:
                self.parent.children.remove(self);
                rawSet(self, 'parent', None);
        

    def __init__(self) -> None:
        LoadDefaultGuiProperties('Instance', self);
        self._ongoingAnimations = [];
        self.internalStore = {};

    def destroy(self):
        self.parent = None;
        signalProperties = [p for p in dir(self) if isinstance(getattr(self, p), LylacSignal)];

        for p in signalProperties:
            sig: LylacSignal = self[p];
            for listener in sig.listeners:
                listener.disconnect();

        for child in self.children:
            child.destroy();

    def update(self):
        pass
    def render(self, dt: float):
        pass

from lylac.modules.defaultGuiProperties import LoadDefaultGuiProperties
from lylac.services.AnimationService import Animation