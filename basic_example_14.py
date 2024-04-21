"""
Example that showcases a very easy way to run blocking code in an asynchronous setting by making use of multiple threads without having to use a specific executor
"""

import asyncio
import logging
import time

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def blocking():
    logger.info("running blocking")
    time.sleep(1)
    logger.info("done blocking")


async def non_blocking():
    logger.info("running non_blocking")
    await asyncio.sleep(1)
    logger.info("done non-blocking")


async def main():
    await asyncio.gather(
        asyncio.to_thread(blocking),
        non_blocking()
    )
    

if __name__ == "__main__":
    logger.info("starting")
    event_loop = asyncio.get_event_loop()
    output = event_loop.run_until_complete(main())
    logger.info("done")