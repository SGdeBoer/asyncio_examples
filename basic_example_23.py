"""
Example showcasing how a simple background thread on which coroutines can be scheduled might work - and how to interact with it using multithreading
"""

import asyncio
import logging
from concurrent.futures import Future, ThreadPoolExecutor
import threading

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


async def operation():
    logger.info("running operation")
    await asyncio.sleep(2)
    logger.info("operation done")
    return 1


class RandomThread(threading.Thread):
    def __init__(self):
        super().__init__(name="test")
        self.loop = asyncio.new_event_loop()

    def run(self):
        self.loop.run_forever()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

    def submit_coro(self, coro):
        future = Future()

        def run():
            logger.info("creating task")
            task = self.loop.create_task(coro)
            logger.info("task created")

            def stuff_to_do_when_done(async_future: asyncio.Future):
                logger.info("entering callback")
                future.set_result(async_future.result())
                logger.info("callback done")

            task.add_done_callback(stuff_to_do_when_done)

        logger.info("running call soon")
        self.loop.call_soon_threadsafe(run)
        logger.info("passed call soon")
        return future.result()


if __name__ == "__main__":
    random_thread = RandomThread()
    random_thread.start()

    with ThreadPoolExecutor() as executor:
        result = executor.map(random_thread.submit_coro, [operation(), operation(), operation()])
    print([r for r in result])

    random_thread.stop()
    random_thread.join()

