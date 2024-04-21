"""
Example on why not to naively trust the event loop to always do the thing you want when it comes to scheduling
"""

import asyncio
import logging
import time
import timeit

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def blocking():
    logger.info("blocking called")
    time.sleep(3)
    logger.info("blocking done")
    pass


async def nonblocking():
    logger.info("nonblocking called")
    await asyncio.sleep(1)
    logger.info("nonblocking done")
    pass


async def amain():
    loop = asyncio.get_running_loop()

    """
    The two operations below take 3 seconds. Why? Since blocking() is a blocking function, you would expect the total sleep
    time to always be 4 seconds, but this is not the case here. The nuance here is that call_soon() schedules something to
    be called on the next iteration of the event loop. In this case a new iteration starts on the await of nonblocking(),
    as this is when the event loop suspends to coro and frees itself up for a new thing to do, which in this case is to
    schedule blocking(). Then while blocking() is running, so is nonblocking(), and the total wait time is as long as blocking()
    """
    logger.info("scheduling blocking and awaiting nonblocking")
    loop.call_soon(blocking)
    await nonblocking()
    logger.info("done")

    """
    The two operations below take 4 seconds. Why? Intuitively we are doing the same as above, but clearly something has happened
    that triggered a new event loop iteration before our calls the nonblocking() actually started. The detail here is that
    the call to gather will create a future and immediately give control back to the event loop, which will then immediately
    invoke the callback we scheduled. This callback is blocking, which means that the future, which we know will take 1
    second to return results, needs to wait for the blocking sleep to be done
    """
    logger.info("scheduling blocking and awaiting a gather")
    loop.call_soon(blocking)
    await asyncio.gather(nonblocking(), nonblocking(), nonblocking())
    logger.info("done")

    pass


if __name__ == "__main__":
    s = timeit.default_timer()
    asyncio.run(amain())
    logger.info(f"elapsed {timeit.default_timer() - s}")