import asyncio

import uvloop
from aiohttp import web


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def handle(request):
    return web.Response(text='Hello world')


async def init():
    """Initialize the application server."""
    app = web.Application()
    app.router.add_routes([web.get('/', handle)])
    return app
