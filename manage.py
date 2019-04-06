import logging

from manager import Manager

from sputnik.main import run_api


LOGGER_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
logging.basicConfig(
    format=LOGGER_FORMAT,
    level=logging.DEBUG,
)


manager = Manager()


@manager.command
def api():
    run_api()


@manager.command
def sandbox():
    async def run():
        pass

    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    manager.main()
