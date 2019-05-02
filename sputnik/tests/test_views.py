from sputnik.main import *


async def test_client(cli):
    resp = await cli.get('/ping')

