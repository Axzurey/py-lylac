import threading
from typing import Any


def rawGet(obj: object, prop: str): return object.__getattribute__(obj, prop);

def rawSet(obj: object, prop: str, value: Any): return object.__setattr__(obj, prop, value);

def createThread(func: Any, *args: Any):

    thr = threading.Thread(target=func, daemon=True, args=args);
    thr.start()

    return thr