"""
Simple example showing it is possible to collect multiple futures and execute them all in a gather, like you would for normal coroutines
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def func():
    logger.info("running func")
    await asyncio.sleep(2)
    logger.info("func done")


async def main():
    logger.info("running main")
    future1 = asyncio.gather(*[func() for _ in range(3)])
    future2 = asyncio.gather(*[func() for _ in range(3)])
    future3 = asyncio.gather(*[func() for _ in range(3)])
    future4 = asyncio.gather(*[func() for _ in range(3)])
    future5 = asyncio.gather(*[func() for _ in range(3)])
    await asyncio.gather(future1, future2, future3, future4, future5)
    logger.info("main done")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logger.info("done")