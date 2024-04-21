"""
Semi-trivial example only supposed to showcase that await blocks the coroutine only, not the entire loop
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


async def gunc():
    logger.info("running gunc")
    _ = sum([i**2 for i in range(int(1e6))])
    logger.info("gunc done")


async def main():
    logger.info("running main")
    await asyncio.gather(*[func(), gunc()])
    logger.info("main done")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logger.info("done")