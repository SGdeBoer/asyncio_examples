"""
Example showcasing interaction of as_completed with a ProcessPoolExecutor for making sure resources are always utilized
"""

import asyncio
import random
import time
from concurrent.futures import ProcessPoolExecutor, Future
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def blocking_call():
    logger.info("running blocking")
    time.sleep(1)
    logger.info("blocking done")
    return 1


async def random_sleep(sleep_time):
    logger.info(f"running coro that sleeps for {sleep_time}")
    await asyncio.sleep(sleep_time)
    return sleep_time


async def amain():
    sleep_times = [random.random() for _ in range(5)]
    logger.info(f"sleep times are {sleep_times}")
    coros = [random_sleep(sleep_time) for sleep_time in sleep_times]

    loop = asyncio.get_event_loop()
    futures: list[Future] = []

    executor = ProcessPoolExecutor(5)

    for coro in asyncio.as_completed(coros):
        result = await coro
        logger.info(f"ready to handle result of coro that slept for {result}")
        futures.append(loop.run_in_executor(executor, blocking_call))

    logger.info("gathering futures")
    results = await asyncio.gather(*futures)
    logger.info("done gathering futures")
    print(results)


if __name__ == "__main__":
    asyncio.run(amain())