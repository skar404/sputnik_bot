from sputnik.models.main import DataBase
from sputnik.settings import TEST_DB_DSN


async def test_ping():
    await DataBase.set_bind(TEST_DB_DSN)
