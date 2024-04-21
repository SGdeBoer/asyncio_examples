"""
Example of running a slow function and a fast function in two different coros with loop.run_forever()
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def func():
    while asyncio.get_running_loop().is_running():
        logger.info("im still here, available to do stuff")
        await asyncio.sleep(1)


async def gunc():
    logger.info("starting the slow function")
    await asyncio.sleep(10)
    logger.info("done with the slow function")
    """
    Now that the slow function is done, the event loop must be stopped, as this is what the fast function is checking on each run.
    If the event loop is not stopped, the fast function will run forever - as the event loop was told to run forever
    """
    asyncio.get_running_loop().stop()


async def main():
    await asyncio.gather(func(), gunc())


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    logger.info("done")