from __future__ import annotations;

from abc import ABC
from typing import TypedDict

import pygame
from modules.keymap import LylacEnum

from modules.lylacSignal import LylacSignal

class InputMouseBuffer(TypedDict):
    position: pygame.Vector2;
    delta: pygame.Vector2;

class InputKeyBuffer(TypedDict):
    key: LylacEnum;

class InputService(ABC):

    lastKeyBuffer: list[InputKeyBuffer] = []; #TODO: INTEROP THIS INTO THE RENDERER!

    _lastMousePosition: pygame.Vector2 = pygame.Vector2();

    onKeyUp = LylacSignal[InputKeyBuffer]();
    onKeyDown = LylacSignal[InputKeyBuffer]();
    
    onMouseButton1Down = LylacSignal[InputMouseBuffer]();
    onMouseButton1Up = LylacSignal[InputMouseBuffer]();
    onMouseButton2Down = LylacSignal[InputMouseBuffer]();
    onMouseButton2Up = LylacSignal[InputMouseBuffer]();

    onMouseMovement = LylacSignal[InputMouseBuffer]();

    @staticmethod
    def isKeyDown(key: LylacEnum):
        pass
