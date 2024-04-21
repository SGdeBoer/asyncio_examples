"""
Example showcasing that it is very easy to end up in a situation where you schedule things and they just quietly never finish
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def short_sleep():
    logger.info("starting short_sleep")
    await asyncio.sleep(2)
    logger.info("short_sleep done")


async def long_sleep():
    logger.info("starting long_sleep")
    await asyncio.sleep(3)
    logger.info("long_sleep done")


async def amain():
    logger.info("starting amain")

    asyncio.create_task(long_sleep())
    await short_sleep()

    """
    Here we have scheduled the coro long_sleep() as a task, which means it will run as soon as the event loop 'has a chance' to run it.
    The first time it gets this chance is when the short_sleep() coro is suspended and scheduled to be continued after 2 seconds.
    However, the task takes 3 seconds, but we have not given it proper time to finish, so it just never does. Instead we run the event
    loop until completion and are left without our scheduled task ever finishing. In order to let it finish, we need to give it enough
    time, and we can do this by awaiting another short_sleep() coro.
    """

    # await short_sleep()
    logger.info("amain done")


if __name__ == "__main__":
    asyncio.run(amain())