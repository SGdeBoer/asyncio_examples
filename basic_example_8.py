"""
Example showcasing that in a ThreadPool each thread can have its own event loop on which you can do things
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import time

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def blocking(number):
    logger.info(f"blocking call number {number}")
    time.sleep(1)
    logger.info(f"blocking call number {number} completed")


def main(number):
    logger.info("entering main")

    """
    asyncio.get_event_loop() does not work because we are not calling main() from the main OS thread, but from newly created threads

    Docs say:
    ---
    If there is no current event loop set in the current OS thread, the OS thread is main, and set_event_loop() has not yet been
    called, asyncio will create a new event loop and set it as the current one.
    ---

    This will not work here because we are in separate threads, so we must create a new event loop per thread. Specifically calling
    asyncio.set_event_loop(loop) is pointless in this context
    """
    loop = asyncio.new_event_loop()
    loop.run_until_complete(blocking(number))
    loop.close()

    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    with ThreadPoolExecutor(3) as pool:
        result = pool.map(main, [1, 2, 3])
    result = [element for element in result]
    logger.info("done")