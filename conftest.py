import asyncio

import pytest
from aiohttp import web

from sputnik.routes import setup_routes


@pytest.fixture()
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop
    loop.close()


async def previous(request):
    if request.method == 'POST':
        request.app['value'] = (await request.post())['value']
        return web.Response(body=b'thanks for the data')
    return web.Response(
        body='value: {}'.format(request.app['value']).encode('utf-8'))


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()

    setup_routes(app)

    return loop.run_until_complete(aiohttp_client(app))
