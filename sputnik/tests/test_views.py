from sputnik.main import *

from conftest import create_app


async def test_client(test_client):
    client = await test_client(create_app)
    resp = await client.get('/ping')
    assert resp.status == 200
