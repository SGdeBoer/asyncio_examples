"""
Example showing that you can technically call asynchronous functions from synchronous ones by just letting the event loop run until completion on each call
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def func(number):
    logger.info(f"coro number {number} is being executed")
    return await asyncio.sleep(1)


def main():
    logger.info("entering main")
    asyncio.get_event_loop().run_until_complete(func(1))
    asyncio.get_event_loop().run_until_complete(func(2))
    asyncio.get_event_loop().run_until_complete(func(3))
    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    main()
    logger.info("done")