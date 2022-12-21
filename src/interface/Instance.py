from __future__ import annotations
from typing import Any
import client.renderer as cliRen
from modules.lylacSignal import LylacSignal
from modules.util import rawSet

class Instance():
    parent: cliRen.Renderer | Instance;
    children: list[Instance];
    

    def __setitem__(self, key: str, value: Any):
        self.__setattr__(key, value);

    def __getitem__(self, key: str):
        return self.__getattribute__(key) or super().__getattribute__(key);

    def __setattr__(self, prop: str, value: Any) -> None:
        if prop == 'parent':
            self.setParent(value);
        else:
            super().__setattr__(prop, value);

    def __getattribute__(self, prop: str):
        return super().__getattribute__(prop);

    def setParent(self, to: cliRen.Renderer | Instance | None):
        if to:
            if self in to.children: return;
            rawSet(self, 'parent', to);
            to.children.append(self);
            print(id(to.children), id(self.children))
        else:
            if self.parent:
                self.parent.children.remove(self);
                rawSet(self, 'parent', None);
        

    def __init__(self) -> None:
        LoadDefaultGuiProperties('Instance', self);

    def update(self, dt: float):
        pass

from modules.defaultGuiProperties import LoadDefaultGuiProperties