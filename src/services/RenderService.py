from __future__ import annotations;
from abc import ABC
from client.renderer import Renderer


class RenderService(ABC):
    renderer: Renderer