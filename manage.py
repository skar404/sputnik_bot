import logging

from manager import Manager

from sputnik.main import run_app


LOGGER_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
logging.basicConfig(
    format=LOGGER_FORMAT,
    level=logging.DEBUG,
)


manager = Manager()


@manager.command
def api():
    run_app(api=True)


@manager.command
def schedule():
    run_app(schedule=True)


@manager.command
def sandbox():
    async def run():
        import weiboapi

        from sputnik.settings import WEIBO_LOGIN, WEIBO_PASSWORD
        from sputnik.clients.weibo_parser import WeiboParserService

        async with WeiboParserService() as weibo_service:
            captcha_data = await weibo_service.login_user(WEIBO_LOGIN, WEIBO_PASSWORD)

            await weibo_service.push_image(captcha_data)
            await weibo_service.create_post('is work : )')

    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    manager.main()
