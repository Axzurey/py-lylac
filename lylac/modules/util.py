import threading;
from typing import Any, Callable, TypeVar;

def rawGet(obj: object, prop: str): return object.__getattribute__(obj, prop);

def rawSet(obj: object, prop: str, value: Any): return object.__setattr__(obj, prop, value);

A = TypeVar("A");

def createThread(func: Callable[[A], Any], *args: A):

    thr = threading.Thread(target=func, daemon=True, args=args);
    thr.start();

    return thr;