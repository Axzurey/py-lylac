from __future__ import annotations;
from abc import ABC
from client.renderer import Renderer
from modules.lylacSignal import LylacSignal


class RenderService(ABC):
    renderer: Renderer
    rendererStarted: bool = False;

    postRender = LylacSignal[float]();