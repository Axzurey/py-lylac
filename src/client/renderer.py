from __future__ import annotations;
import pygame;
import time

from interface.Instance import Instance;

class Renderer():
    framerate: int;
    rendererClosing: bool = False;
    lastUpdate: float = 0;
    currentFrameEvents: list[pygame.event.Event] = [];
    screen: pygame.surface.Surface;

    children: list[Instance]

    def __init__(self, resolution: tuple[int, int], framerate: int = 60) -> None:
        self.framerate = framerate;

        self.screen = pygame.display.set_mode(resolution);

    def start(self):
        clock = pygame.time.Clock();

        while not self.rendererClosing:
            now = time.time();

            dt = now - self.lastUpdate;

            self.lastUpdate = now;

            events = pygame.event.get()
            self.currentFrameEvents = events;

            self.screen.fill((0, 0, 0)) #this goes before you update ui elements

            pygame.display.flip();

            clock.tick(self.framerate);