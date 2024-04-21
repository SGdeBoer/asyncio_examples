"""
Basic example showcasing that a semaphore can be used to limit the amount of coroutines that run concurrently
"""

import asyncio
import logging
import random

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def func(semaphore):
    async with semaphore:
        runtime = random.random() * 5
        logger.info(f"running func with runtime {runtime}")

        """
        this is meant to mimic arbitrary operations that can take any amount of integer seconds between 1 and 5
        """

        await asyncio.sleep(runtime)
        logger.info(f"func done with runtime {runtime}")


async def main():
    logger.info("running main")
    semaphore = asyncio.Semaphore(5)
    coros = [func(semaphore) for _ in range(10)]
    await asyncio.gather(*coros)
    logger.info("main done")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logger.info("done")