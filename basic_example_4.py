"""
Basic example with blocking code and how you cannot just wrap it inside tasks to be executed concurrently
"""

import asyncio
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


async def main():
    logger.info("entering main")
    # the blocking function is called inside the create_task call here and since it has no return value
    # this results in create_task being called with None argument, which throws
    # this showcases how synchronous code cannot naively be intertwined with asynchronous programming
    tasks = [asyncio.create_task(blocking(i)) for i in range(10)]
    await asyncio.gather(*tasks)
    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logger.warning(f"exception got raised: {e.args[0]}")
    logger.info("done")