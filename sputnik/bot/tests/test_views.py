

async def test_command_start(cli):
    request = await cli.post('/bot', json={

    })
    request_json = await request.json()

    assert request.status == 200
