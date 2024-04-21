"""
Example showcasing how create_task works and how to check for an execption thrown in a task
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def func():
    logger.info("entering gunc")
    await asyncio.sleep(1)
    raise Exception("error")


async def main():
    """
    create_task submits a coro to the event loop for execution concurrently with other tasks, the point of
    switching being any await. This means we can either await the task if we really need it the be done
    or we can await something like an asyncio.sleep (or any other awaitable) if we don't care about the result
    in this case the task lasts 1 second and thus finishes on a 1.1 second sleep, after which we can look at
    its exception
    """
    task = asyncio.create_task(func())
    await asyncio.sleep(1.1)
    print(task.exception())
    """
    awaiting the task directly will just raise the exception, which is probably the desired outcome if you
    choose to await it directly - however with create_task you can clearly run a multitude of things in the
    background and then deal with them later, for example by adding a callback_when_done to the task
    """



if __name__ == "__main__":
    logger.info("starting")
    event_loop = asyncio.get_event_loop()
    output = event_loop.run_until_complete(main())
    logger.info("done")