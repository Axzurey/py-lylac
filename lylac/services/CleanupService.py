from lylac.interface.Instance import Instance;
import asyncio;
from typing import Callable, Any;

class CleanupService:
    @staticmethod
    async def cleanUp(obj: Instance, after: float, beforeDestroy: Callable[[], Any]):
        """
        obj is the object to cleanup
        after is the time in seconds to cleanup
        """
        await asyncio.sleep(after);
        beforeDestroy();
        obj.destroy();