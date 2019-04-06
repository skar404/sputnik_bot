from aiohttp import web


async def ping(_request):
    return web.json_response({
        'success': True,
        'result': 'pong'
    })
