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
        from sputnik.settings import WEIBO_LOGIN, WEIBO_PASSWORD
        from sputnik.clients.weibo_parser import WeiboParserService
        from sputnik.clients.anti_captcha import AntiCaptchaService

        weibo_service = WeiboParserService()

        auth = await weibo_service.get_server_data_in_login(WEIBO_LOGIN)
        auth.password = WEIBO_PASSWORD
        await weibo_service.update_auth_data_set_password_secret(auth)

        data = await weibo_service.login_user(auth)
        breakpoint()

    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    manager.main()
