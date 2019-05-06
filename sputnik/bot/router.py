from dataclasses import dataclass


class MessageType:
    COMMAND = 'command'
    TEXT = 'text'
    OTHER = 'other'
    CALLBACK_QUERY = 'callback_query'


@dataclass
class BotFutureRoute:
    handler: object
    message_type: MessageType.mro()
    key: object


class TelegramRouterException(Exception):
    pass


class TelegramRouter:
    all_key = '*'

    def __init__(self, bot_token):
        self.routes = []
        self.register_routers = {}
        self.bot_token = bot_token

    def get_uri(self, message_type: str, key=None):
        if key is None:
            key = self.all_key
        return '{type}://{key}'.format(type=message_type, key=key)

    def get_uri_in_message(self, message):
        if 'message' in message:
            if 'text' in message['message']:
                text: str = message['message']['text']
                if text[0] == '/':
                    return self.get_uri(message_type=MessageType.COMMAND, key=text[1:].strip())
                else:
                    return self.get_uri(message_type=MessageType.TEXT)
        elif 'callback_query' in message:
            if 'data' in message['callback_query']:
                callback_key = message['callback_query']['data'].split(':')[:-1]
                if callback_key:
                    callback_key = ':'.join(callback_key)
                    return self.get_uri(message_type=MessageType.CALLBACK_QUERY, key=callback_key)

        return self.get_uri(message_type=MessageType.OTHER)

    async def init_route(self, message, request=None):
        uri = self.get_uri_in_message(message)
        if self.register_routers.get(uri):
            request['uri'] = uri
            return await self.register_routers[uri].handler(message, request)

    def register(self, ignore_uniq=True):
        for route in self.routes:
            uri = self.get_uri(message_type=route.message_type, key=route.key)

            if uri not in self.register_routers:
                self.register_routers[uri] = route
            else:
                if not ignore_uniq:
                    raise TelegramRouterException('routes is not unique', uri)

    def register_route(self, message_type: MessageType.mro(), key=None):
        def decorator(fun):

            self.routes.append(BotFutureRoute(
                handler=fun,
                message_type=message_type,
                key=key
            ))

        return decorator

    def command(self, command):
        return self.register_route(
            message_type=MessageType.COMMAND,
            key=command
        )

    def text(self):
        return self.register_route(
            message_type=MessageType.TEXT,
        )

    def callback_query(self, callback_key):
        return self.register_route(
            message_type=MessageType.CALLBACK_QUERY,
            key=callback_key
        )
