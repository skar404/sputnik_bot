import logging

from manager import Manager

from sputnik.main import run_app


LOGGER_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
logging.basicConfig(
    format=LOGGER_FORMAT,
    level=logging.DEBUG,
)


manager = Manager()


@manager.command
def api():
    run_app(api=True)


@manager.command
def schedule():
    run_app(schedule=True)


@manager.command
def sandbox():
    async def run():
        pass

    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    manager.main()
