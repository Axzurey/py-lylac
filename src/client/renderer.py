from __future__ import annotations
from typing import Literal, Optional, TypedDict;
import pygame;
import pygame.freetype;
import time
from interface.Instance import Instance
from interface.NominalObjects import Clickable, Hoverable
from modules.keymap import KeyBuffer, purifyRawKeyBuffer
from modules.lylacSignal import LylacSignal
from services.InputService import InputService;

pygame.init();
pygame.freetype.init();

buttonTypeMap: list[Literal['right'] | Literal['left'] | Literal['middle'] | Literal['scrollUp'] | Literal['scrollDown']] = [
    'left', 'left', 'middle', 'right', 'scrollUp', 'scrollDown']; #the first left is not used but needed to be included.

class RendererListeners(TypedDict):
    keyUp: LylacSignal[KeyBuffer];
    keyDown: LylacSignal[KeyBuffer];

class ActionPassList(TypedDict):
    mouseLifted: bool
    mousePressed: bool
    mouseScrolling: bool
    mouseScrollDirection: pygame.Vector2

class ActionOrder(TypedDict):
    at: float
    obj: Instance

class ActionOrdersT(TypedDict):
    hover: list[ActionOrder]
    click: list[ActionOrder]

class MouseClickBuffer(TypedDict):
    position: pygame.Vector2
    clickType: Literal['right'] | Literal['left'] | Literal['middle'] | Literal['scrollUp'] | Literal['scrollDown']

class UpdateBuffer(TypedDict):
    mouseBuffer: MouseClickBuffer | None
    actionOrders: ActionOrdersT
    actionList: ActionPassList
    lastButton: ActionOrder | None

FreeColorTuple = tuple[int, int, int, Optional[int]]

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

        self.children = [];

    def recurseUpdate(self, inst: Instance, dt: float, update: UpdateBuffer) -> UpdateBuffer:
        inst.update(dt)

        childrenPriority: list[Instance] = []
        childrenLast: list[Instance] = []

        for child in inst.children:
            if type(child["zindex"]) is int:
                childrenPriority.append(child)
            else:
                childrenLast.append(child)

        childrenPriority.sort(key=lambda x: x["zindex"]);

        for child in childrenPriority:
            if issubclass(type(child), Clickable):
                update['actionOrders']['click'].append({"obj": child, "at": time.time()})

                if update['mouseBuffer']:

                    t = time.time()
                    if child.isPointInBounding(update['mouseBuffer']['position']):
                        update['lastButton'] = {'at': t, 'obj': child}

            if issubclass(type(child), Hoverable):
                update['actionOrders']['hover'].append({"obj": child, "at": time.time()})

            update = self.recurseUpdate(child, dt, update);

        for child in childrenLast:
            if issubclass(type(child), Clickable):
                update['actionOrders']['click'].append({"obj": child, "at": time.time()})

                if update['mouseBuffer']:

                    t = time.time()
                    if child.isPointInBounding(update['mouseBuffer']['position']):
                        update['lastButton'] = {'at': t, 'obj': child}

            if issubclass(type(child), Hoverable):
                update['actionOrders']['hover'].append({"obj": child, "at": time.time()})

            update = self.recurseUpdate(child, dt, update)

        return update

    def start(self):
        clock = pygame.time.Clock();

        while not self.rendererClosing:
            now = time.time();

            dt = now - self.lastUpdate;

            self.lastUpdate = now;

            events = pygame.event.get()
            self.currentFrameEvents = events;

            self.screen.fill((0, 0, 0)) #this goes before you update ui elements

            passList: ActionPassList = {
                "mouseLifted": False,
                "mousePressed": False,
                "mouseScrolling": False,
                "mouseScrollDirection": pygame.Vector2(),
            }

            keysUp: list[int] = []
            keysDown: list[int] = []
            modifiers: list[int] = []

            mouseBuffer: MouseClickBuffer | None = None;

            for event in events:
                if event.type == pygame.QUIT:

                    self.rendererClosing = True;

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    passList['mousePressed'] = True;
                    mouseBuffer = {
                        'position': pygame.Vector2(event.pos),
                        'clickType': buttonTypeMap[event.button],
                    }

                elif event.type == pygame.MOUSEBUTTONUP:

                    passList['mouseLifted'] = True;
                    mouseBuffer = {
                        'position': pygame.Vector2(event.pos),
                        'clickType': buttonTypeMap[event.button],
                    }
                    
                elif event.type == pygame.MOUSEWHEEL:

                    passList['mouseScrolling'] = True
                    passList["mouseScrollDirection"] = pygame.Vector2(event.x, event.y)

                elif event.type == pygame.KEYDOWN:

                    keysDown.append(event.key)
                    if not event.mod in modifiers:
                        modifiers.append(event.mod)

                elif event.type == pygame.KEYUP:

                    keysUp.append(event.key)
                    if not event.mod in modifiers:
                        modifiers.append(event.mod)


            upKeyBuffer = purifyRawKeyBuffer({
                "keys": keysUp,
                "modifiers": modifiers
            })
            
            downKeyBuffer = purifyRawKeyBuffer({
                "keys": keysDown,
                "modifiers": modifiers
            })

            if len(downKeyBuffer['keys']) != 0:
                InputService.onKeyDown.dispatch(downKeyBuffer);
            if len(upKeyBuffer['keys']) != 0:
                InputService.onKeyUp.dispatch(upKeyBuffer);

            old = InputService.__lastMousePosition;

            if mouseBuffer:
                deltaMovement = mouseBuffer['position'] - old;
                InputService.__lastMousePosition = mouseBuffer['position'];
                InputService.onMouseMovement.dispatch({
                    "position": mouseBuffer['position'],
                    "delta": deltaMovement #type: ignore this would still work.
                });

            for child in self.children:
                updBfr = self.recurseUpdate(child, dt, {
                    "actionOrders": {
                        'hover': [],
                        'click': []
                    },
                    "actionList": passList,
                    "mouseBuffer": mouseBuffer,
                    "lastButton": None
                })

                # there you go. it works, so now implement it c:
                if (updBfr['lastButton']):
                    print(updBfr['lastButton']['obj'], 'clicked!')

            pygame.display.flip();

            clock.tick(self.framerate);