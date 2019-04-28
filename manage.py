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
    run_app(name='api', api=True, port=8080)


@manager.command
def schedule():
    run_app(name='schedule', schedule=True, port=8081)


@manager.command
def sandbox():
    async def run():
        import base64

        from sputnik.settings import WEIBO_LOGIN, WEIBO_PASSWORD
        from sputnik.clients.weibo_parser import WeiboParserService

        cookies = None

        async with WeiboParserService() as weibo_service:
            await weibo_service.login_user(WEIBO_LOGIN, WEIBO_PASSWORD)
            breakpoint()
            # with open('test_data/kate.jpg', 'rb') as f:
            #     photo_bit = base64.b64encode(f.read())
            # photo_id = await weibo_service.get_id_and_push_image(photo_bit, 'test')
            # await weibo_service.create_post('is work : )', photo_id)

    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    manager.main()
