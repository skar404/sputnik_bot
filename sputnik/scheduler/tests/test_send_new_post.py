from sputnik.scheduler.utils import ping


async def test_ping(cli):
    await ping()
