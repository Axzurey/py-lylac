import math
from typing import Any, Sequence 
from pygame import Vector2
from modules.color4 import clamp

from modules.lylacSignal import LylacSignal

def isPointInCircle(point: Vector2, circleOrigin: Vector2, circleRadius: float) -> bool:
    return (point - circleOrigin).magnitude() < circleRadius;

def isRightOrOn(p0: Vector2, p1: Vector2, point: Vector2) -> bool:
    #https://stackoverflow.com/questions/1560492/how-to-tell-whether-a-point-is-to-the-right-or-left-side-of-a-line
    fx = p1.x - p0.x;
    fy = p1.y - p0.y;

    t = fx * (point.y - p0.y) - fy * (point.x - p0.x);

    if t > 0: # > 0 is on the left side.
        return False;
    return True;

def rotatedCorner(point: Vector2, centerOfRotation: Vector2, theta: float) -> Vector2:
    #https://gamedev.stackexchange.com/questions/86755/how-to-calculate-corner-positions-marks-of-a-rotated-tilted-rectangle
    tX = point.x - centerOfRotation.x;
    tY = point.y - centerOfRotation.y;

    theta = math.radians(theta);

    rotatedX = tX * math.cos(theta) - tY * math.sin(theta);
    rotatedY = tX * math.sin(theta) + tY * math.cos(theta);

    return Vector2(rotatedX + centerOfRotation.x, rotatedY + centerOfRotation.y);

def isPointInPolygon(vertices: Sequence[Vector2], point: Vector2):
    for i in range(len(vertices)):
        vertex = vertices[i];
        nextIndex = 0 if i == len(vertices) - 1 else i + 1
        nextVertex = vertices[nextIndex]
        if isRightOrOn(vertex, nextVertex, point):
            return False;
    return True;


def isPointInRotatedBounding(pos: Vector2, size: Vector2, point: Vector2, cornerRadius: float, rotation: float):
    unrotatedCorners = [
        pos, pos + Vector2(size.x, 0),
        pos + size, pos + Vector2(0, size.y)
    ];

    #for now, we'll assume the center of the object is the center of rotation
    corners = [rotatedCorner(p, pos + size / 2, -rotation) for p in unrotatedCorners];

    cornersContainingPoints = [not isRightOrOn(v[0], v[1], point) for v in [
        (corners[0], corners[1]),
        (corners[1], corners[2]),
        (corners[2], corners[3]),
        (corners[3], corners[0])
    ]]; #for some reason this is reversed?

    isPointInRectBounds = cornersContainingPoints.count(False) == 0;

    if not isPointInRectBounds: return False;
    
    #https://math.stackexchange.com/questions/2207331/finding-the-fourth-point-of-a-perfect-square-without-knowing-order-of-points
    cornerIndex = 0;
    for corner in corners:
        
        rI = 0 if cornerIndex == 3 else cornerIndex + 1;
        uI = 3 if cornerIndex == 0 else cornerIndex - 1;
        right = corners[rI];
        up = corners[uI];

        rightPush = corner + (right - corner).normalize() * cornerRadius;
        upPush = corner + (up - corner).normalize() * cornerRadius;

        center = pos + size / 2;

        directionToCenter = (center - corner).normalize();

        lengthToCenterOfSquare = math.sqrt(2 * cornerRadius ** 2);

        centerPointOfSquare = corner + directionToCenter * (lengthToCenterOfSquare / 2);

        lastVertex = 4 * centerPointOfSquare - (rightPush + upPush + corner);

        if isPointInPolygon([upPush, corner, rightPush, lastVertex], point) and not isPointInCircle(point, lastVertex, cornerRadius):
            return False;

        cornerIndex += 1;
    return True;


def isPointInBounding(pos: Vector2, size: Vector2, point: Vector2, cornerRadius: float) -> bool:
    bottomR = pos + size - Vector2(cornerRadius, cornerRadius);
    bottomL = pos + Vector2(0, size.y) + Vector2(cornerRadius, -cornerRadius);
    topR = pos + Vector2(size.x, 0) + Vector2(-cornerRadius, cornerRadius);
    topL = pos + Vector2(cornerRadius, cornerRadius);

    if point.x > (pos + size).x or point.y > (pos + size).y: 
        return False;
    if point.x < pos.x or point.y < pos.y: 
        return False;

    if point.x > bottomR.x and point.y > bottomR.y:
        return isPointInCircle(point, bottomR, cornerRadius);
    elif point.x > topR.x and point.y < topR.y:
        return isPointInCircle(point, topR, cornerRadius);
    elif point.x < bottomL.x and point.y > bottomL.y:
        return isPointInCircle(point, bottomL, cornerRadius);
    elif point.x < topL.x and point.y < topL.y:
        return isPointInCircle(point, bottomL, cornerRadius);

    return True;


class HasBounding:
    def isPointInBounding(self: Any, point: Vector2):
        return isPointInRotatedBounding(self.absolutePosition, self.absoluteSize, point, clamp(self.cornerRadius, 0, min(self.absoluteSize.x, self.absoluteSize.y)), self.rotation)

class Hoverable(HasBounding):
    onHoverEnter: LylacSignal;
    onHoverExit: LylacSignal;

    _isHover: bool = False;

    def __init__(self) -> None:
        super().__init__();

        self.onHoverEnter = LylacSignal();
        self.onHoverExit = LylacSignal();

class Clickable(HasBounding):
    onMouseButton1Down: LylacSignal[None];
    onMouseButton1Up: LylacSignal[None];
    onMouseButton2Down: LylacSignal[None];
    onMouseButton2Up: LylacSignal[None];

    _isMouse1Down: bool = False;
    _isMouse2Down: bool = False;
    
    def __init__(self) -> None:
        super().__init__();
        
        self.onMouseButton1Down = LylacSignal[None]();
        self.onMouseButton1Up = LylacSignal[None]();
        self.onMouseButton2Down = LylacSignal[None]();
        self.onMouseButton2Up = LylacSignal[None]();