import logging
from asyncio import TaskGroup

from src.common.decorators import run_forever

logger = logging.getLogger(__name__)


class SampleBackgroundWorker:
    def __init__(self):
        self._is_running = False

    async def run(self):
        async with TaskGroup() as tg:
            tg.create_task(self._background_task1())
            tg.create_task(self._background_task2())

    @run_forever(interval=60)
    async def _background_task1(self):
        logger.info("Background task 1")

    @run_forever(interval=30, initial_wait=15)
    async def _background_task2(self):
        logger.info("Background task 2")
