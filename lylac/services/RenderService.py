from __future__ import annotations
from typing import Callable, Any;
from lylac.modules.lylacSignal import LylacSignal

post_render_calls = {};

def PostRender(identifier: str):
    def get_function(func: Callable[[float], Any]):
        if identifier in post_render_calls:
            raise Exception(f"identifier {identifier} is already registered. This should be unique");
        post_render_calls[identifier] = func;
    return get_function;

def RemoveFromPostRenderQueue(identifier: str):
    """
        returns true if the function associated with the identifier was removed from the render queue.
        returns false otherwise.
    """
    if identifier in post_render_calls:
        del post_render_calls[identifier];
        return True;
    return False;

class RenderService:
    from lylac.client.renderer import Renderer
    renderer: Renderer
    rendererStarted: bool = False;

    postRender = LylacSignal[float]();
    renderBegin = LylacSignal();

    _preliminary_update_calls = ["update", "update_image", "update_surfaces", "recalculate_surface_positions_for_position_change"];

def update_render_calls(dt: float):
    for callK in list(post_render_calls):
        post_render_calls[callK](dt);

RenderService.postRender.connect(update_render_calls);