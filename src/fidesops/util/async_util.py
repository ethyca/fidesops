import asyncio
from typing import TypeVar, Callable, Any, Awaitable, Optional
import logging

logger = logging.getLogger(__name__)
T = TypeVar("T")


def run_async(task: Callable[[Any], T], *args, **kwargs) -> Awaitable[T]:
    """Run a callable async"""
    loop = asyncio.get_event_loop()
    if callable(task):
        return loop.run_in_executor(None, task, *args, **kwargs)
    else:
        raise TypeError("Task must be a callable")


def wait_for(t: Awaitable[T]) -> Optional[T]:
    """Wait for the return of a callable. This is mostly intended
    to be used for testing async tasks."""
    try:
        return asyncio.get_event_loop().run_until_complete(t)
    except Exception as e:
        logger.error(e)
