from aiohttp import web

from sputnik.routes import setup_routes


def run_api():
    app = web.Application()
    setup_routes(app)
    web.run_app(app)
