import logging

from aiohttp import web

from sputnik.routes import setup_routes


async def init_telegram(_app):
    from sputnik.clients.telegram.client import TelegramSDK
    req = (await TelegramSDK().update_web_hook())
    assert req.json['ok']
    logging.info('update telegram web hook url')


def run_api():
    app = web.Application()

    app.on_startup.append(init_telegram)

    setup_routes(app)
    web.run_app(app)
