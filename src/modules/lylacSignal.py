from __future__ import annotations;
from typing import Generic, TypeVar, Callable;

A = TypeVar("A");

class LylacConnection(Generic[A]):
    callback: Callable[[A], None];
    signal: LylacSignal[A];

    def __init__(self, callback: Callable[[A], None], signal: LylacSignal[A]) -> None:
        self.callback = callback;
        self.signal = signal;

    def disconnect(self):
        try:
            self.signal.listeners.remove(self)
        except ValueError:
            return;

class LylacSignal(Generic[A]):

    listeners: list[LylacConnection[A]];

    def __init__(self):
        self.listeners = [];

    def connect(self, callback: Callable[[A], None]) -> LylacConnection:
        ...