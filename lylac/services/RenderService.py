from __future__ import annotations;
from abc import ABC
from lylac.modules.lylacSignal import LylacSignal


class RenderService(ABC):
    from lylac.client.renderer import Renderer
    renderer: Renderer
    rendererStarted: bool = False;

    postRender = LylacSignal[float]();