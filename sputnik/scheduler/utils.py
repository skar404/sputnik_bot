from sputnik.models.main import DataBase


async def ping(app):
    await DataBase.scalar('SELECT 1;')
