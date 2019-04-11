import time
import asyncio
import concurrent.futures
from functools import partial


def sleep():
    time.sleep(5)
    print('sleep')


def not_block():
    print('not_block')


async def main(loop, executo):
    loop = asyncio.get_running_loop()
    await asyncio.wait(
        fs={
            # Returns after delay=12 seconds
            loop.run_in_executor(executor, sleep),

            # Returns after delay=14 seconds
            loop.run_in_executor(executor, sleep),

            # Returns after delay=16 seconds
            loop.run_in_executor(executor, sleep),

            loop.run_in_executor(executo, not_block)
        },
        return_when=asyncio.ALL_COMPLETED
    )
    print('main')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    loop.run_until_complete(main(loop, executor))
    print('__main__')
