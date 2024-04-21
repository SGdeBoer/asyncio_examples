"""
Simple example showcasing how to use a ThreadPoolExecutor to execute blocking code in a multithreaded way while maintaining asynchronous functionality
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import time

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def blocking(number):
    logger.info(f"blocking call number {number}")
    time.sleep(1)
    logger.info(f"blocking call number {number} completed")


async def main(executor):
    logger.info("entering main")
    loop = asyncio.get_running_loop()
    _ =  await asyncio.wait([
        loop.run_in_executor(executor, blocking, 1),
        loop.run_in_executor(executor, blocking, 2),
        loop.run_in_executor(executor, blocking, 3),
    ])
    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    executor = ThreadPoolExecutor(3)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(executor))
    logger.info("done")