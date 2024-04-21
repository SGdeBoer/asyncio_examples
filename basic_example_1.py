"""
Most basic asyncio example with creating coroutines and gathering them, showcasing the concurrent behavior

Important to understand what `await` actually does. It pauses execution of the current async function until a specified
coroutine has been completed. If that coroutine calls another coroutine, the current coroutine gets suspended and a
context switch occurs. The context of the current coroutine is saved and the context of a called coroutine is loaded.

With this in mind it is obvious why something like:

await asyncio.sleep(1)
await asyncio.sleep(1)

takes 2 seconds, while something like:

await asyncio.gather(asyncio.sleep(1), asyncio.sleep(1))

takes only 1 second
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