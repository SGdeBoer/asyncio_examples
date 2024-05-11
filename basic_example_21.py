"""
Example showcasing a simple as_completed use case, where you can handle results as soon as they're done rather than in the order they were scheduled
"""

import asyncio
import random
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def random_sleep(sleep_time):
    logger.info(f"running coro that sleeps for {sleep_time}")
    await asyncio.sleep(sleep_time)
    return sleep_time


async def amain():
    sleep_times = [random.random() * 5 for _ in range(5)]
    logger.info(f"sleep times are {sleep_times}")
    coros = [random_sleep(sleep_time) for sleep_time in sleep_times]

    for coro in asyncio.as_completed(coros):
        result = await coro
        logger.info(f"ready to handle result of coro that slept for {result}")


if __name__ == "__main__":
    asyncio.run(amain())