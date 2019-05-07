from sputnik.bot.router import TelegramRouter, MessageType, BotFutureRoute


def test_get_uri():
    uri = TelegramRouter(bot_token=None).get_uri(message_type=MessageType.COMMAND, key='start')

    assert uri == 'command://start'


def test_get_uri_in_message_message():
    telegram_router = TelegramRouter(bot_token=None)

    message = {
        'message': {
            'text': 'присет мир'
        }
    }

    uri_message = telegram_router.get_uri_in_message(message)
    assert uri_message == 'text://*'


def test_get_uri_in_message_command():
    telegram_router = TelegramRouter(bot_token=None)

    message = {
        'message': {
            'text': '/start'
        }
    }

    uri_message = telegram_router.get_uri_in_message(message)
    assert uri_message == 'command://start'


def test_get_uri_in_message_callback_query():
    telegram_router = TelegramRouter(bot_token=None)

    message = {
        'callback_query': {
            'data': 'setting:open:id:1'
        }
    }

    uri_message = telegram_router.get_uri_in_message(message)
    assert uri_message == 'callback_query://setting:open:id'


def test_get_uri_in_message_other():
    telegram_router = TelegramRouter(bot_token=None)

    message = {
        'test': 'other'
    }

    uri_message = telegram_router.get_uri_in_message(message)
    assert uri_message == 'other://*'


def fun_return_data(key):
    async def fun(message, request):
        return key, message, request
    return fun


async def test_init_route():
    telegram_router = TelegramRouter(bot_token=None)

    command_start = telegram_router.get_uri(message_type=MessageType.COMMAND, key='start')
    message_text = telegram_router.get_uri(message_type=MessageType.TEXT)
    callback_query = telegram_router.get_uri(message_type=MessageType.TEXT)

    telegram_router.register_routers = {
        command_start: BotFutureRoute(
            handler=fun_return_data('command_start'),
            message_type=None,
            key=None
        ),
        message_text: BotFutureRoute(
            handler=fun_return_data('message_text'),
            message_type=None,
            key=None
        ),
        callback_query: BotFutureRoute(
            handler=fun_return_data('callback_query'),
            message_type=None,
            key=None
        ),
    }

    message = {
        'message': {
            'text': 'привет мир'
        }
    }

    router_fun = await telegram_router.init_route(message, request={})

    assert router_fun == ('callback_query', {'message': {'text': 'привет мир'}}, {'uri': 'text://*'})
