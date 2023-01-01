from __future__ import annotations
from typing import Any, Dict, Literal
from pygame import Vector2
import pygame
from lylac.interface.Instance import Instance
from lylac.interface.NominalObjects import NominalObject
from lylac.modules.color4 import Color4
from lylac.modules.udim2 import Udim2
from lylac.modules.util import rawSet
import uuid

def blankAnyTypedList() -> list[Any]:
    return list()

GUI_DEFAULT_PROPERTIES = {
    "parent": lambda: None,
    "children": lambda: blankAnyTypedList(),
    "absoluteSize": lambda: Vector2(),
    "absolutePosition": lambda: Vector2(),
    "size": lambda: Udim2.fromOffset(150, 50),
    "position": lambda: Udim2.fromOffset(0, 0),
    "backgroundColor": lambda: Color4(.8, .8, 0),
    "borderColor": lambda: Color4(1, 0, 1),
    "cornerRadius": lambda: 15,
    "borderWidth": lambda: 5,
    "dropShadowColor": lambda: Color4(.2, .2, .2),
    "dropShadowRadius": lambda: 5,
    "dropShadowOffset": lambda: Udim2.fromOffset(2, 2),
    "text": lambda: 'Hello World!',
    "textColor": lambda: Color4(.5, .5, .5),
    "textSize": lambda: 16,
    "textFont": lambda: "notosansmono-regular",
    "textAlignX": lambda: "left",
    "textAlignY": lambda: "top",
    "zIndex": lambda: 1,
    "boundingRect": lambda: pygame.Rect(0, 0, 0, 0),
    "rotation": lambda: 0,
    "points": lambda: [Vector2(150, 75), Vector2(300, 150), Vector2(150, 200), Vector2(400, 400)],
    "color": lambda: Color4(0, 1, 1),
    "width": lambda: 15,
    "showControlPoints": lambda: True,
    "imagePath": lambda: 'lylac/images/lilac.png',
    "curvePoints": lambda: [],
    "anchorPoint": lambda: Vector2(),
    "controlPointColor": lambda: Color4(0, 0, 1),
    "controlPointRadius": lambda: 10,
    "relativeSize": lambda: 'xy',
    "relativePosition": lambda: 'xy',
    "name": lambda: f"instance-{uuid.uuid4().hex}"
}

GUI_PROPERTY_MAP: dict[str, Dict[Literal['properties'] | Literal["inherits"], list[str]]] = {
    "Instance": {
        "properties": ["children", "name"],
    },
    "Frame": {
        "properties": []
    },
    "NurbsObject": {
        "properties": ["points", "color", "width", "showControlPoints", "controlPointColor", "controlPointRadius"]
    },
    "DraggableNurbsObject": {
        "properties": ["points", "color", "width", "curvePoints"]
    },
    "PolygonObject": {
        "properties": ["points", "color", "width", "showControlPoints", "controlPointColor", "controlPointRadius"]
    },
    "DraggablePolygonObject": {
        "properties": ["points", "color", "width"]
    },
    "SegmentedLineObject": {
        "properties": ["points", "color", "width", "showControlPoints", "controlPointColor", "controlPointRadius"]
    },
    "DraggableSegmentedLineObject": {
        "properties": ["points", "color", "width"]
    },
    "Sprite": {
        "properties": [
            "size", "position", "absoluteSize", 
            "absolutePosition", "rotation", "boundingRect",
            "imagePath", "anchorPoint", "relativeSize",
            "relativePosition"
        ]
    },
    "SupportsOrdering": {
        "properties": ["zIndex"]
    },
    "GuiObject": {
        "properties": [
            "size", "position", "backgroundColor",
            "borderColor", "borderWidth", "dropShadowColor", 
            "dropShadowRadius", "dropShadowOffset", "absolutePosition",
            "absoluteSize", "cornerRadius", "boundingRect",
            "rotation", "anchorPoint", "relativeSize",
            "relativePosition"
        ],
        "inherits": ["Instance"]
    },
    "TextObject": {
        "properties": ["text", "textColor", "textSize", "textFont", "textAlignX", "textAlignY"],
        "inherits": ["GuiObject"]
    },
    "TextLabel": {
        "properties": [],
        "inherits": ["TextObject"]
    },
    "ImageButton": {
        "properties": ["imagePath"]
    },
    "TextButton": {
        "properties": [],
        "inherits": ["TextObject"]
    },
    "EmptyButton": {
        "properties": []
    }
}

def LoadDefaultGuiProperties(guiType: str, guiObject: Instance | NominalObject):
    if GUI_PROPERTY_MAP[guiType]:
        #load own properties
        for propKey in GUI_PROPERTY_MAP[guiType]["properties"]:
            if propKey in GUI_DEFAULT_PROPERTIES:
                rawSet(guiObject, propKey, GUI_DEFAULT_PROPERTIES[propKey]())
            else:
                raise Exception(f"property {propKey} is not a valid property in the Default Properties map!");
        return GUI_PROPERTY_MAP[guiType]["properties"];

    else:
        raise Exception(f"guiType {guiType} is not a valid type in the property map!")
