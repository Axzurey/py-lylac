from __future__ import annotations
from abc import ABC
from enum import Enum
from pygame import Vector2
from typing import Callable, TypeVar, Generic
import math

import pygame

from lylac.interface.Instance import Instance
from lylac.modules.color4 import Color4
from lylac.modules.lylacSignal import LylacConnection
from lylac.modules.mathf import denormalize, lerp, clamp, normalize
from lylac.modules.udim2 import Udim2
from lylac.services.RenderService import RenderService

class InterpolationMode(Enum):
    linear = "linear";

    easeInSine = "easeInSine";
    easeOutSine = "easeOutSine";
    easeInOutSine = "easeInOutSine";

    easeInCubic = "easeInCubic";
    easeOutCubic = "easeOutCubic";
    easeInOutCubic = "easeInOutCubic";

    easeInQuint = "easeInQuint";
    easeOutQuint = "easeOutQuint";
    easeInOutQuint = "easeInOutQuint";

    easeInCirc = "easeInCirc";
    easeOutCirc = "easeOutCirc";
    easeInOutCirc = "easeInOutCirc";

    easeInElastic = "easeInElastic";
    easeOutElastic = "easeOutElastic";
    easeInOutElastic = "easeInOutElastic";

c4 = (2 * math.pi) / 3;
c5 = (2 * math.pi) / 4.5;

TIME_INTERPOLATIONS: dict[InterpolationMode, Callable[[float], float]] = {
    InterpolationMode.linear: lambda t: t,

    InterpolationMode.easeInSine: lambda t: 1 - math.cos((t * math.pi) / 2),
    InterpolationMode.easeOutSine: lambda t: math.sin((t * math.pi) / 2),
    InterpolationMode.easeInOutSine: lambda t: -(math.cos(math.pi * t) - 1) / 2,

    InterpolationMode.easeInCubic: lambda t: t * t * t,
    InterpolationMode.easeOutCubic: lambda t: 1 - math.pow(1 - t, 3),
    InterpolationMode.easeInOutCubic: lambda t: 4 * t * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 3) / 2,

    InterpolationMode.easeInQuint: lambda t: t * t * t * t * t,
    InterpolationMode.easeOutQuint: lambda t: 1 - math.pow(1 - t, 5),
    InterpolationMode.easeInOutQuint: lambda t: 16 * t * t * t * t * t if t < .5 else 1 - math.pow(-2 * t + 2, 5) / 2,

    InterpolationMode.easeInCirc: lambda t: 1 - math.sqrt(1 - math.pow(t, 2)),
    InterpolationMode.easeOutCirc: lambda t: math.sqrt(1 - math.pow(t - 1, 2)),
    InterpolationMode.easeInOutCirc: lambda t: (1 - math.sqrt(1 - math.pow(2 * t, 2))) / 2 if t < .5 else (math.sqrt(1 - math.pow(-2 * t + 2, 2)) + 1) / 2,

    InterpolationMode.easeInElastic: lambda t: 0 if t == 0 else 1 if t == 1 else -math.pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * c4),
    InterpolationMode.easeOutElastic: lambda t: 0 if t == 0 else 1 if t == 1 else math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1,
    InterpolationMode.easeInOutElastic: lambda t: 0 if t == 0 else 1 if t == 1 else -(math.pow(2, 20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2 if t < .5 else (math.pow(2, -20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1
}

T = TypeVar("T", pygame.Vector2, float, Color4, Udim2)

class Animation(Generic[T]):

    targetObject: Instance
    origin: T;
    target: T;
    value: T;
    animationLength: float;
    interpolationMode: InterpolationMode;
    timeValue: float;
    onUpdate: Callable[[T], None];

    renderConnection: LylacConnection[float];

    def __init__(
        self,
        origin: T,
        target: T,
        animationLength: float,
        interpolationMode: InterpolationMode,
        onUpdate: Callable[[T], None]
    ) -> None:
        
        self.renderConnection = RenderService.postRender.connect(lambda f: self.update(f));

        self.value = origin;
        self.origin = origin;
        self.target = target;
        self.animationLength = animationLength;
        self.interpolationMode = interpolationMode;
        self.onUpdate = onUpdate;
        self.timeValue = 0;

    def disconnect(self):
        self.renderConnection.disconnect();

    def update(self, dt: float):
        self.timeValue += dt;
        tV = clamp(0, self.animationLength, self.timeValue);

        timeDelta = tV / self.animationLength;

        trueTime = TIME_INTERPOLATIONS[self.interpolationMode](timeDelta);

        match self.origin:
            case pygame.Vector2():
                self.value = self.origin.lerp(self.target, trueTime)
            case Color4():
                self.value = self.origin.lerp(self.target, trueTime)
            case float() | int():
                self.value = lerp(self.origin, self.target, trueTime) #type: ignore
            case Udim2():
                self.value = self.origin.lerp(self.target, trueTime);
            case _:
                raise Exception(type(self.origin) + " is not a supported type!");

        self.onUpdate(self.value);

        if self.timeValue >= self.animationLength:
            self.disconnect();

class AnimationService(ABC):
    ...

    @staticmethod
    def createAnimation(
        obj: Instance,
        property: str,
        targetValue: T,
        animationDuration: float,
        interpolationMode: InterpolationMode = InterpolationMode.linear
    ):

        def setValue(t: T):
            obj[property] = t;

        originalValue: T = obj[property];

        if originalValue == targetValue: return;

        anim = Animation(originalValue, targetValue, animationDuration, interpolationMode, setValue);
        obj._ongoingAnimations.append(anim);

        return anim;
