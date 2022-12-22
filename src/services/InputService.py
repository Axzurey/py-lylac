from __future__ import annotations;

from abc import ABC
from typing import TypedDict

import pygame
from modules.keymap import KeyCode

from modules.lylacSignal import LylacSignal

class InputMouseBuffer(TypedDict):
    position: pygame.Vector2;
    delta: pygame.Vector2;

class InputKeyBuffer(TypedDict):
    key: KeyCode;

class InputService(ABC):

    lastKeyDownBuffer: list[InputKeyBuffer] = []; #TODO: INTEROP THIS INTO THE RENDERER!

    _lastMousePosition: pygame.Vector2 = pygame.Vector2();

    _isMouseButton1Down = False;
    _isMouseButton2Down = False;

    onKeyUp = LylacSignal[InputKeyBuffer]();
    onKeyDown = LylacSignal[InputKeyBuffer]();
    
    onMouseButton1Down = LylacSignal[InputMouseBuffer]();
    onMouseButton1Up = LylacSignal[InputMouseBuffer]();
    onMouseButton2Down = LylacSignal[InputMouseBuffer]();
    onMouseButton2Up = LylacSignal[InputMouseBuffer]();

    onMouseMovement = LylacSignal[InputMouseBuffer]();

    @staticmethod
    def isMouse1Down():
        return InputService._isMouseButton1Down;

    @staticmethod
    def isMouse2Down():
        return InputService._isMouseButton2Down;

    @staticmethod
    def isKeyDown(key: KeyCode):
        if key in map(lambda x: x['key'], InputService.lastKeyDownBuffer):
            return True;
        return False;