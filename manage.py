from aiohttp import web


async def handle(_request):
    return web.Response(text='Hello world')


def init():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    web.run_app(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    init()
