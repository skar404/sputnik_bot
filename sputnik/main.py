import logging
import ssl

import sentry_sdk
from aiohttp import web
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from sputnik import settings
from sputnik.models.main import DataBase
from sputnik.routes import setup_routes
from sputnik.scheduler.main import init_jobs


async def setup_telegram(app: web.Application):
    from sputnik.clients.telegram.client import TelegramSDK
    req = (await TelegramSDK().update_web_hook())
    assert req.json['ok']
    logging.info('update telegram web hook url')


async def setup_data_base(app: web.Application):
    ctx = ssl.create_default_context(capath='./.postgresql.pem')
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    await DataBase.set_bind(settings.DB_DSN, ssl=None)


def init_app(name: str, api: bool = False, schedule: bool = False, update_web_hook: bool = False):
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[AioHttpIntegration()],
        environment=settings.ENVIRONMENT,
        release=settings.DRONE_COMMIT,
        server_name=name,
    )

    app: web.Application = web.Application()

    ctx = ssl.create_default_context(capath='./.postgresql.pem')
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    app.on_startup.append(setup_data_base)

    if api is True:
        if update_web_hook:
            app.on_startup.append(setup_telegram)
        setup_routes(app)

    if schedule is True:
        scheduler = init_jobs(app)
        scheduler.start()
    return app


def run_app(port, name, api=False, schedule=False, update_web_hook=False):
    web.run_app(init_app(name, api, schedule, update_web_hook), port=port)
