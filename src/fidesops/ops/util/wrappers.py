import asyncio
from functools import wraps
from typing import Any, Callable


def sync(func: Callable) -> Any:
    """Converts an async function into a sync function."""

    @wraps(func)
    def wrap(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(func(*args, **kwargs))

    return wrap
