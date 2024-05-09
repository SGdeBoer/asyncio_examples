"""
Example of a function decorator that allows for profiling/timing coroutines
"""

import asyncio
import timeit
import logging
from typing import Callable, Any

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def time_await(func: Callable) -> Callable:
    async def wrapped(*args, **kwargs) -> Any:
        logger.info(f"running {func.__name__} with args {args} {kwargs}")
        start = timeit.default_timer()
        try:
            return await func(*args, **kwargs)
        finally:
            end = timeit.default_timer()
            total = end - start
            logger.info(f"finished {func.__name__} in {total}s")
    return wrapped


@time_await
async def dummy_operation():
    logger.info("starting dummy operation")
    await asyncio.sleep(3)
    logger.info("finished dummy operation")


@time_await
async def main():
    await asyncio.gather(dummy_operation(), dummy_operation())


if __name__ == "__main__":
    asyncio.run(main())