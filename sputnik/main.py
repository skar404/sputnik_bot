import logging
import ssl

from aiohttp import web
from asyncpg.pool import Pool

from sputnik import settings
from sputnik.clients.weibo_parser import WeiboAuthData
from sputnik.models.main import DataBase
from sputnik.routes import setup_routes
from sputnik.scheduler.main import init_jobs


class WebApp(web.Application):
    db_pool: Pool
    weibo_login: WeiboAuthData
    weibo_login_test: WeiboAuthData


async def init_telegram():
    from sputnik.clients.telegram.client import TelegramSDK
    req = (await TelegramSDK().update_web_hook())
    assert req.json['ok']
    logging.info('update telegram web hook url')


async def init_app(api=False, schedule=False):
    app = WebApp()

    ctx = ssl.create_default_context(capath='./.postgresql.pem')
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    await DataBase.set_bind(settings.DB_DSN, ssl=ctx)

    if api is True:
        await init_telegram()
        setup_routes(app)

    if schedule is True:
        scheduler = init_jobs(app)
        scheduler.start()

    return app


def run_app(port, api=False, schedule=False,):
    web.run_app(init_app(api, schedule), port=port)
