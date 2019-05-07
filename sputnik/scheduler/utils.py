from sputnik.models.main import DataBase


async def ping():
    await DataBase.scalar('SELECT 1;')
