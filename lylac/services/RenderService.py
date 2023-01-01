from __future__ import annotations;
from abc import ABC
from lylac.modules.lylacSignal import LylacSignal


class RenderService(ABC):
    from lylac.client.renderer import Renderer
    renderer: Renderer
    rendererStarted: bool = False;

    postRender = LylacSignal[float]();
    renderBegin = LylacSignal();

    _preliminary_update_calls = ["update", "update_image", "update_surfaces", "recalculate_surface_positions_for_position_change"];