from __future__ import annotations
from typing import Literal, TypedDict;
import pygame;
import pygame.freetype;
import time
from lylac.interface.NominalObjects import Clickable, Hoverable, SupportsOrdering
from lylac.modules.keymap import KeyBuffer, purifyRawKeyBuffer
from lylac.modules.lylacSignal import LylacSignal
from lylac.services.DebugService import DebugService

pygame.init();
pygame.freetype.init();

buttonTypeMap: list[Literal["NONE"] | Literal['right'] | Literal['left'] | Literal['middle'] | Literal['scrollUp'] | Literal['scrollDown']] = [
    'NONE', 'left', 'middle', 'right', 'scrollUp', 'scrollDown']; #the first left is not used but needed to be included.

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
    clickType: Literal['right'] | Literal['left'] | Literal['middle'] | Literal['scrollUp'] | Literal['scrollDown'] | Literal["NONE"]

class UpdateBuffer(TypedDict):
    mouseBuffer: MouseClickBuffer | None;
    actionOrders: ActionOrdersT;
    actionList: ActionPassList;
    lastButton: ActionOrder | None;
    lastHover: ActionOrder | None;

class Renderer():
    
    framerate: int;
    rendererClosing: bool = False;
    lastUpdate: float = 0;
    currentFrameEvents: list[pygame.event.Event] = [];
    screen: pygame.surface.Surface;
    resolution: tuple[int, int];

    children: list[Instance]

    def __init__(self, resolution: tuple[int, int], framerate: int = 60) -> None:
        self.framerate = framerate;

        self.screen = pygame.display.set_mode(resolution);

        self.children = [];
    
        self.resolution = resolution;

        FontService.loadDefaultFonts();

        RenderService.renderer = self;

    def recurseUpdate(self, inst: Instance, dt: float, update: UpdateBuffer) -> UpdateBuffer:
        inst.render(dt)

        childrenPriority: list[Instance] = [];
        childrenLast: list[Instance] = [];

        for child in inst.children:
            if isinstance(child, SupportsOrdering) and type(child["zIndex"]) is int:
                childrenPriority.append(child);
            else:
                childrenLast.append(child);

        childrenPriority.sort(key=lambda x: x["zIndex"]);

        for child in childrenLast:
            if issubclass(type(child), Clickable):
                update['actionOrders']['click'].append({"obj": child, "at": time.time()});

                if update['mouseBuffer'] and update['mouseBuffer']['clickType'] in ('left', 'right'):

                    t = time.time()
                    if child.isPointInBounding(update['mouseBuffer']['position']):
                        update['lastButton'] = {'at': t, 'obj': child}

            if issubclass(type(child), Hoverable):
                update['actionOrders']['hover'].append({"obj": child, "at": time.time()});
                
                if update['mouseBuffer']:

                    t = time.time();

                    if child.isPointInBounding(update['mouseBuffer']['position']):
                        update['lastHover'] = {'at': t, 'obj': child};

            update = self.recurseUpdate(child, dt, update)

        for child in childrenPriority:

            if issubclass(type(child), Clickable):
                update['actionOrders']['click'].append({"obj": child, "at": time.time()})

                if update['mouseBuffer'] and update['mouseBuffer']['clickType'] in ('left', 'right'):

                    t = time.time()
                    if child.isPointInBounding(update['mouseBuffer']['position']):
                        update['lastButton'] = {'at': t, 'obj': child}

            if issubclass(type(child), Hoverable):
                update['actionOrders']['hover'].append({"obj": child, "at": time.time()});

                if update['mouseBuffer']:

                    t = time.time();
                    if child.isPointInBounding(update['mouseBuffer']['position']):
                        update['lastHover'] = {'at': t, 'obj': child};


            update = self.recurseUpdate(child, dt, update);

        return update

    def shortUpdate(self, child: Instance):
        for c in RenderService._preliminary_update_calls:
            if hasattr(child.__class__, c) and callable(getattr(child.__class__, c)):
                getattr(child.__class__, c)(child);
        for c in child.children:
            self.shortUpdate(c);

    def start(self):

        self.lastUpdate = time.time();

        clock = pygame.time.Clock();

        RenderService.rendererStarted = True;

        for child in self.children:
            self.shortUpdate(child);

        RenderService.renderBegin.dispatch(None);

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
                    
                    if event.button < 5:

                        passList['mousePressed'] = True;
                        
                        mouseBuffer = {
                            'position': pygame.Vector2(event.pos),
                            'clickType': buttonTypeMap[event.button],
                        }

                elif event.type == pygame.MOUSEBUTTONUP:

                    if event.button < 5:
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
                    #if not event.mod in modifiers:
                        #modifiers.append(event.mod)

                elif event.type == pygame.KEYUP:

                    keysUp.append(event.key)
                    #if not event.mod in modifiers:
                       # modifiers.append(event.mod)

            if not mouseBuffer:
                mouseBuffer = {'position': pygame.Vector2(pygame.mouse.get_pos()), 'clickType': 'NONE'}

            upKeyBuffer = purifyRawKeyBuffer({
                "keys": keysUp,
                "modifiers": modifiers
            })
            
            downKeyBuffer = purifyRawKeyBuffer({
                "keys": keysDown,
                "modifiers": modifiers
            })

            if len(downKeyBuffer['keys']) != 0:
                for key in downKeyBuffer['keys']:
                    InputService.onKeyDown.dispatch({"key": key});
            if len(upKeyBuffer['keys']) != 0:
                for key in upKeyBuffer['keys']:
                    InputService.onKeyUp.dispatch({"key": key});

            old = InputService._lastMousePosition;
            InputService.lastKeyDownBuffer = [{'key': v} for v in downKeyBuffer['keys']];

            if mouseBuffer:
                deltaMovement = mouseBuffer['position'] - old;
                InputService._lastMousePosition = mouseBuffer['position'];

                positionalData: InputMouseBuffer = {
                    "position": mouseBuffer['position'],
                    "delta": deltaMovement #type: ignore this would still work.
                };

                InputService.onMouseMovement.dispatch(positionalData);

                if mouseBuffer['clickType'] == 'left':
                    InputService._isMouseButton1Down = True if passList['mousePressed'] else False;
                    if passList['mousePressed']:
                        InputService.onMouseButton1Down.dispatch(positionalData);
                    else:
                        InputService.onMouseButton1Up.dispatch(positionalData);
                elif mouseBuffer['clickType'] == 'right':
                    InputService._isMouseButton2Down = True if passList['mousePressed'] else False;
                    if passList['mousePressed']:
                        InputService.onMouseButton2Down.dispatch(positionalData);
                    else:
                        InputService.onMouseButton2Up.dispatch(positionalData);

            for child in self.children:
                updBfr = self.recurseUpdate(child, dt, {
                    "actionOrders": {
                        'hover': [],
                        'click': []
                    },
                    "actionList": passList,
                    "mouseBuffer": mouseBuffer,
                    "lastButton": None,
                    "lastHover": None
                });

                for aOrder in updBfr['actionOrders']['click']:

                    child = aOrder['obj'];
                    if issubclass(type(child), Clickable) and not updBfr['lastButton'] or ((updBfr['lastButton'] and child != updBfr['lastButton']['obj']) or False):
                        if child._isMouse1Down and not InputService.isMouse1Down():
                            child._isMouse1Down = False;
                            child.onMouseButton1Up.dispatch(None);
                        if child._isMouse2Down and not InputService.isMouse2Down():
                            child._isMouse2Down = False;
                            child.onMouseButton2Up.dispatch(None);

                for aOrder in updBfr['actionOrders']['hover']:

                    child = aOrder['obj'];

                    if issubclass(type(child), Hoverable) and not updBfr['lastHover'] or ((updBfr['lastHover'] and child != updBfr['lastHover']['obj']) or False):
                        if child._isHover:
                            child._isHover = False;
                            child.onHoverExit.dispatch(None);

                # there you go. it works, so now implement it c:
                if updBfr['lastButton']:
                    if mouseBuffer and mouseBuffer['clickType'] == 'left' and passList['mousePressed'] and updBfr['lastButton']['obj'].enabled:
                        updBfr['lastButton']['obj'].onMouseButton1Down.dispatch(None);
                        updBfr['lastButton']['obj']._isMouse1Down = True;
                    elif mouseBuffer and mouseBuffer['clickType'] == 'right' and passList['mousePressed'] and updBfr['lastButton']['obj'].enabled:
                        updBfr['lastButton']['obj'].onMouseButton2Down.dispatch(None);
                        updBfr['lastButton']['obj']._isMouse2Down = True;
                if updBfr['lastHover']:
                    if hasattr(updBfr['lastHover']['obj'], "canHover") and updBfr['lastHover']['obj'].canHover:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND);
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW);
                    if not updBfr['lastHover']['obj']._isHover:
                        updBfr['lastHover']['obj'].onHoverEnter.dispatch(None);
                        updBfr['lastHover']['obj']._isHover = True;
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW);

            
            if len(DebugService.points) > 0:
                surf = pygame.Surface(self.resolution, pygame.SRCALPHA, 32);
                surf = surf.convert_alpha();
                    
                for point in DebugService.points:
                    
                    pygame.draw.circle(surf, point.color.toRGBTuple(), point.vertex, 5);
                    if not point.static:
                        point.remove();
                self.screen.blit(surf, (0, 0))

            RenderService.postRender.dispatch(dt);

            pygame.display.flip();
            pygame.display.set_caption(f"Blind Nue [@{str(round(clock.get_fps()))}fps]");
            clock.tick(self.framerate);

from lylac.services.InputService import InputMouseBuffer, InputService
from lylac.services.RenderService import RenderService;
from lylac.services.FontService import FontService;

from lylac.interface.GuiObject import GuiObject
from lylac.interface.Instance import Instance