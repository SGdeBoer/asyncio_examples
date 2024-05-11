"""
Example showcasing why using run_until_complete to avoid marking functions as async is not good practice
"""

import asyncio
import time
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def heavy_task():
    logger.info("heavy task running")
    time.sleep(10)


async def light_task():
    await asyncio.sleep(1)


def main():
    loop = asyncio.new_event_loop()

    logger.info("scheduling heavy task")
    task = loop.create_task(heavy_task())
    logger.info("done scheduling heavy task")

    logger.info("running light task till completion")
    loop.run_until_complete(light_task())
    logger.info("done running light task")


if __name__ == "__main__":
    main()
    exit(0)
