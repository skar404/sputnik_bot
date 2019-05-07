from sputnik.scheduler.utils import ping


async def test_ping():
    await ping(app=None)
