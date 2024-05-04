"""
Example showcasing wait_for functionality with explicitly creating tasks
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def random_operation():
    logger.info("random operation start")
    await asyncio.sleep(10)
    logger.info("random operation finish")


async def main():
    task = asyncio.create_task(random_operation())
    try:
        result = await asyncio.wait_for(task, timeout=2)
    except asyncio.exceptions.TimeoutError:
        logger.info("timed out")


if __name__ == "__main__":
    asyncio.run(main())