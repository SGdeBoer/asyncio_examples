"""
Example with writing to a file, sleeping, and then reading from the same file
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def func(number):
    logger.info(f"coro number {number} is being executed")
    with open ("temp.txt", "w") as out:
        out.write(f"coro {number}")

    await asyncio.sleep(1)

    with open ("temp.txt", "r") as out:
        logger.info(f"read {out.read()}")


async def main():
    logger.info("entering main")
    coros = [func(i) for i in range(10)]
    await asyncio.gather(*coros)
    logger.info("done with main")


if __name__ == "__main__":
    logger.info("starting")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logger.info("done")