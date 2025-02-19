from asyncio import sleep
import logging
import functools


logger = logging.getLogger(__name__)


def run_forever(interval: float = 60, initial_wait: float = 0):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            await sleep(initial_wait)
            while True:
                try:
                    await func(*args)
                except Exception as e:
                    logger.warning(f"Exception raised in coroutine: {func.__name__} - coroutine will continue to run", exc_info=e)
                await sleep(interval)
        return wrapped
    return wrapper
