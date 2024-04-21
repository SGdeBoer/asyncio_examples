"""
Example that uses coros containing blocking code and non blocking code and showcases what blocking/non-blocking actually means
"""

import asyncio
import logging
import time

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def blocking_sleep(number):
    logger.info(f"blocking call number {number}")
    time.sleep(1)
    logger.info(f"blocking call number {number} completed")


async def non_blocking_sleep(number):
    logger.info(f"non blocking call number {number}")
    await asyncio.sleep(1)
    logger.info(f"non blocking call number {number} completed")


async def main():
    logger.info("entering main")
    tasks_with_blocking = [blocking_sleep(i) for i in range(3)]
    tasks_without_blocking = [non_blocking_sleep(i) for i in range(3)]
    await asyncio.gather(*tasks_with_blocking)
    await asyncio.gather(*tasks_without_blocking)
    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logger.info("done")