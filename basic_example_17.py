"""
Example showcasing that creating coroutines to set up for an efficient gather call is at risk of going completely wrong when
working with references instead of copies
"""

import asyncio
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Summer:
    def __init__(self, x):
        self.x = x

    async def calculate(self, y):
        return self.x + y


async def amain():
    summer = Summer(1)
    coros = []
    coros_shifted = []
    for number in [1, 2, 3]:
        coros.append(summer.calculate(number))
        summer.x += 1
        coros_shifted.append(summer.calculate(number))
    results = await asyncio.gather(*coros)
    results_shifted = await asyncio.gather(*coros_shifted)
    return results, results_shifted


if __name__ == "__main__":
    results, results_shifted = asyncio.run(amain())
    print(results)
    print(results_shifted)
