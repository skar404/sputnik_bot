from sputnik.main import *


async def test_client(cli):
    # await DataBase.set_bind(TEST_DB_DSN)
    request = await cli.get('/ping')

    data = await request.json()

    assert request.status == 200
    assert data == {'status': 'SUCCESS', 'result': 'pong'}


async def test_bot_bad_request(cli):
    request = await cli.post('/bot')
    data = await request.json()

    assert request.status == 400
    assert data == {'status': 'ERROR', 'error': 'error decode json'}

    request = await cli.post('/bot', json={'test': 'test'})
    data = await request.json()

    assert request.status == 400
    assert data == {'status': 'ERROR', 'errors': {'test': ['Unknown field.']}}


async def test_bot_success_request(cli):
    request = await cli.post('/bot', json={})
    data = await request.json()

    assert request.status == 200
    assert data == {'status': 'SUCCESS'}
