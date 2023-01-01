from __future__ import annotations
import math
from typing import Any, Sequence 
from pygame import Vector2
from lylac.modules.color4 import Color4
from lylac.modules.mathf import clamp
from lylac.modules.lylacSignal import LylacSignal
from lylac.services.DebugService import DebugService

class line:
    def __init__(self, p1: Vector2, p2: Vector2):
        self.p1 = p1
        self.p2 = p2

def onLine(l1, p):
    # Check whether p is on the line or not
    if (
        p.x <= max(l1.p1.x, l1.p2.x)
        and p.x <= min(l1.p1.x, l1.p2.x)
        and (p.y <= max(l1.p1.y, l1.p2.y) and p.y <= min(l1.p1.y, l1.p2.y))
    ):
        return True
    return False
 
def direction(a, b, c):
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0:
        # Colinear
        return 0
    elif val < 0:
        # Anti-clockwise direction
        return 2
    # Clockwise direction
    return 1
 
def isIntersect(l1, l2):
    # Four direction for two lines and points of other line
    dir1 = direction(l1.p1, l1.p2, l2.p1)
    dir2 = direction(l1.p1, l1.p2, l2.p2)
    dir3 = direction(l2.p1, l2.p2, l1.p1)
    dir4 = direction(l2.p1, l2.p2, l1.p2)
 
    # When intersecting
    if dir1 != dir2 and dir3 != dir4:
        return True
 
    # When p2 of line2 are on the line1
    if dir1 == 0 and onLine(l1, l2.p1):
        return True
 
    # When p1 of line2 are on the line1
    if dir2 == 0 and onLine(l1, l2.p2):
        return True
 
    # When p2 of line1 are on the line2
    if dir3 == 0 and onLine(l2, l1.p1):
        return True
 
    # When p1 of line1 are on the line2
    if dir4 == 0 and onLine(l2, l1.p2):
        return True
 
    return False
 
def isPointInPolygon(poly: list[Vector2], p: Vector2):
    #https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
    #more reliable than testing if it lies to the right of each line?
    n = len(poly);
    if n < 3:
        return False
 
    exline = line(p, Vector2(9999, p.y))
    count = 0
    i = 0
    while True:
        side = line(poly[i], poly[(i + 1) % n])
        if isIntersect(side, exline):
            if (direction(side.p1, p, side.p2) == 0):
                return onLine(side, p);
            count += 1
         
        i = (i + 1) % n;
        if i == 0:
            break
 
    # When count is odd
    return count & 1;

def isPointInPolygonSidecheck(vertices: Sequence[Vector2], point: Vector2):
    for i in range(len(vertices)):
        vertex = vertices[i];
        nextIndex = 0 if i == len(vertices) - 1 else i + 1
        nextVertex = vertices[nextIndex]
        if isRightOrOn(vertex, nextVertex, point):
            return False;
    return True;

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

        dR = (right - corner).normalize();
        dU = (up - corner).normalize();

        directionToCenter = dU.lerp(dR, .5).normalize();

        lengthToCenterOfSquare = math.sqrt(2 * cornerRadius ** 2);

        centerPointOfSquare = corner + directionToCenter * (lengthToCenterOfSquare / 2);

        lastVertex = 4 * centerPointOfSquare - (rightPush + upPush + corner);

        if isPointInPolygonSidecheck([upPush, corner, rightPush, lastVertex], point) and not isPointInCircle(point, lastVertex, cornerRadius):
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


class NominalObject: ...

class CanEnable:
    enabled: bool;
    def __init__(self) -> None:
        self.enabled = True;

class HasBounding(NominalObject):
    def isPointInBounding(self: Any, point: Vector2):
        from lylac.interface.GuiObject import GuiObject
        cRadius = clamp(0, min(self.absoluteSize.x, self.absoluteSize.y), self.cornerRadius) if isinstance(self, GuiObject) else 0; #type: ignore

        return isPointInRotatedBounding(self.absolutePosition, self.absoluteSize, point, cRadius, self.rotation)

class IsPolygonal(NominalObject):
    def isPointInPolygon(self, point: Vector2):
        points: list[Vector2] = self.points; #type: ignore

        return isPointInPolygon(points, point);

class SupportsOrdering(NominalObject):
    zIndex: int;

    def __init__(self) -> None:
        self.zIndex = 1;

class Hoverable(HasBounding):
    onHoverEnter: LylacSignal;
    onHoverExit: LylacSignal;

    _isHover: bool = False;

    def __init__(self) -> None:
        HasBounding.__init__(self);

        self.onHoverEnter = LylacSignal();
        self.onHoverExit = LylacSignal();

class Clickable(HasBounding, CanEnable):
    onMouseButton1Down: LylacSignal[Any];
    onMouseButton1Up: LylacSignal[Any];
    onMouseButton2Down: LylacSignal[Any];
    onMouseButton2Up: LylacSignal[Any];

    _isMouse1Down: bool = False;
    _isMouse2Down: bool = False;
    
    def __init__(self) -> None:
        HasBounding.__init__(self);
        CanEnable.__init__(self);
        
        self.onMouseButton1Down = LylacSignal[Any]();
        self.onMouseButton1Up = LylacSignal[Any]();
        self.onMouseButton2Down = LylacSignal[Any]();
        self.onMouseButton2Up = LylacSignal[Any]();