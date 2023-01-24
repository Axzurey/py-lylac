from __future__ import annotations
import time;
from typing import Any, Generic, TypeVar, Callable

from lylac.modules.util import createThread;

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

    def wait(self, pollingRate: int = 60, breakCondition: Callable[[], bool | None] | None = None) -> list[A] | None:
        """
        If you use the breakcondition parameter, then you can expect to get a "None" return value when it returns true;
        """
        conArgs: list[A] = [];
        conFired = False;

        def setFired(*args: Any):
            nonlocal conFired, conArgs;
            conFired = True;
            conArgs = [*args];

        connection = LylacConnection(setFired, self, True);
        self.listeners.append(connection);

        while not conFired:
            if breakCondition and breakCondition():
                return None;
            time.sleep(1 / pollingRate);
        return conArgs

    def connect(self, callback: Callable[[A], Any]) -> LylacConnection:
        connection = LylacConnection(callback, self);
        self.listeners.append(connection);
        return connection;

    def once(self, callback: Callable[[A], Any]) -> LylacConnection:
        connection = LylacConnection(callback, self, True);
        self.listeners.append(connection);
        return connection;
    
    def dispatch(self, *args: A):
        if not args:
            args = [None] #type: ignore
        toremove: list[LylacConnection] = [];
        for listener in self.listeners:
            createThread(listener.callback, *args);
            if listener.once:
                toremove.append(listener);

        for listener in toremove:
            listener.disconnect();