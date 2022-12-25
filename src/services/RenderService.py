from __future__ import annotations;
from abc import ABC
from modules.lylacSignal import LylacSignal


class RenderService(ABC):
    from client.renderer import Renderer
    renderer: Renderer
    rendererStarted: bool = False;

    postRender = LylacSignal[float]();