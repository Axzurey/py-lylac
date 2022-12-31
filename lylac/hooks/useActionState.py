from typing import Any
from lylac.interface.Instance import Instance
from lylac.interface.NominalObjects import Clickable, Hoverable
from lylac.modules.lylacSignal import LylacConnection


def useActionState(
    obj: Instance,
    defaultProperties: dict[str, Any],
    hoverProperties: dict[str, Any] = {},
    leftClickProperties: dict[str, Any] = {},
    rightClickProperties: dict[str, Any] = {}
):

    isHover = False;
    isMouse1 = False;
    isMouse2 = False;

    connections: list[LylacConnection] = [];

    def modify():
        if isMouse1:
            for property in leftClickProperties:
                obj[property] = leftClickProperties[property];
        elif isMouse2:
            for property in rightClickProperties:
                obj[property] = rightClickProperties[property];
        elif isHover:
            for property in hoverProperties:
                obj[property] = hoverProperties[property];
        else:
            for property in defaultProperties:
                obj[property] = defaultProperties[property];

    def setHover(t: bool):
        nonlocal isHover;
        isHover = t;
        modify();

    def setMouse1(t: bool):
        nonlocal isMouse1;
        isMouse1 = t;
        modify();

    def setMouse2(t: bool):
        nonlocal isMouse2;
        isMouse2 = t;
        modify();

    if isinstance(obj, Hoverable) and len(hoverProperties.keys()) > 0:
        connEnter = obj.onHoverEnter.connect(lambda _: setHover(True));
        connExit = obj.onHoverExit.connect(lambda _: setHover(False));

        connections.extend((connEnter, connExit));

    if isinstance(obj, Clickable):
        if len(leftClickProperties.keys()) > 0:
            clickStart1 = obj.onMouseButton1Down.connect(lambda _: setMouse1(True));
            clickEnd1 = obj.onMouseButton1Up.connect(lambda _: setMouse1(False));

            connections.extend((clickStart1, clickEnd1));
        if len(rightClickProperties.keys()) > 0:
            clickStart2 = obj.onMouseButton2Down.connect(lambda _: setMouse2(True));
            clickEnd2 = obj.onMouseButton2Up.connect(lambda _: setMouse2(False));

            connections.extend((clickStart2, clickEnd2));

    def disconnect():
        for connection in connections:
            connection.disconnect();

    return {
        "disconnect": disconnect,
        "isAlive": lambda: len(connections) > 0
    }