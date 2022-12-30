from __future__ import annotations;
from typing import Any, Generic, TypeVar, Callable

from modules.util import createThread;

A = TypeVar("A");

class LylacConnection(Generic[A]):
    callback: Callable[[A], None];
    signal: LylacSignal[A];
    connected: bool = False;
    once: bool = False;

    def __init__(self, callback: Callable[[A], Any], signal: LylacSignal[A], once: bool = False) -> None:
        self.callback = callback;
        self.signal = signal;
        self.connected = True;
        self.once = once;

    def disconnect(self):
        if not self.connected: return;
        try:
            self.signal.listeners.remove(self);
            self.connected = False;
        except ValueError:
            return;

class LylacSignal(Generic[A]):

    listeners: list[LylacConnection[A]];

    def __init__(self):
        self.listeners = [];

    def connect(self, callback: Callable[[A], Any]) -> LylacConnection:
        connection = LylacConnection(callback, self);
        self.listeners.append(connection);
        return connection;

    def once(self, callback: Callable[[A], Any]) -> LylacConnection:
        connection = LylacConnection(callback, self, True);
        self.listeners.append(connection);
        return connection;
    
    def dispatch(self, *args: A):
        for listener in self.listeners:
            createThread(listener.callback, *args);
            if listener.once:
                listener.disconnect();