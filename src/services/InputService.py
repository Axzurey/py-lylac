from __future__ import annotations;

from abc import ABC
from typing import TypedDict

import pygame
from modules.keymap import KeyBuffer

from modules.lylacSignal import LylacSignal

class MouseBuffer(TypedDict):
    position: pygame.Vector2;
    delta: pygame.Vector2;

class InputService(ABC):

    __lastMousePosition: pygame.Vector2 = pygame.Vector2();

    onKeyUp = LylacSignal[KeyBuffer]();
    onKeyDown = LylacSignal[KeyBuffer]();
    
    onMouseButton1Down = LylacSignal[MouseBuffer]();
    onMouseButton1Up = LylacSignal[MouseBuffer]();
    onMouseButton2Down = LylacSignal[MouseBuffer]();
    onMouseButton2Up = LylacSignal[MouseBuffer]();

    onMouseMovement = LylacSignal[MouseBuffer]();