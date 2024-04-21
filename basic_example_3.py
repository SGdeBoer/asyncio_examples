"""
Not very relevant but still interesting example around stopping a running event loop - and registering when exactly it is and is not stopped
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def main():
    logger.info("entering main")
    loop = asyncio.get_running_loop()
    loop.stop()
    logger.info(f"loop is running: {loop.is_running()}")
    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        logger.info(f"loop is running: {loop.is_running()}")
    except Exception as e:
        logger.warning(f"Exception got raised {e.args[0]}")
    logger.info("done")