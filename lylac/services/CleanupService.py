from lylac.interface.Instance import Instance;
import threading;
import time;
from typing import Callable, Any, TypeVar;

background_tasks = set();

T = TypeVar("T")

class CleanupService:

    @staticmethod
    def delay(after: float, callback: Callable[[T], Any], *args: T):
        thread = threading.Thread(target=lambda args: (time.sleep(after), callback(args)), daemon=True, args=args);
        thread.start();

    @staticmethod
    def _perform_static_cleanup(obj: Instance, after: float, beforeDestroy: Callable[[], Any] | None = None):
        time.sleep(after);
        if beforeDestroy:
            beforeDestroy();
        obj.destroy();

    @staticmethod
    def cleanUp(obj: Instance, after: float, beforeDestroy: Callable[[], Any] | None = None):
        thread = threading.Thread(target=CleanupService._perform_static_cleanup, daemon=True, args=(obj, after, beforeDestroy));
        thread.start();