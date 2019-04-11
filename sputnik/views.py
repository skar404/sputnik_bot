import jwt
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from jwt import DecodeError

from sputnik.bot.views import bot_handler
from sputnik.clients.telegram.schema import WebHookMessageSchema
from sputnik.clients.weibo_api import WeiboService
from sputnik.models.main import DataBase
from sputnik.settings import JWT_SECRET
from sputnik.shortcuts.validation import validation_shame
from sputnik.shortcuts.view import success, bad_request


async def ping(request):
    await DataBase.scalar('SELECT 1;')

    return success('pong')


async def waibo(request):
    state = request.query.get('state')
    code = request.query.get('code')
    if not state and not code:
        return bad_request()

    try:
        jwt_data = jwt.decode(state, JWT_SECRET)
    except DecodeError:
        return bad_request()

    req = await WeiboService().oauth_user(code)

    return success()


@validation_shame(WebHookMessageSchema)
async def bot(request: Request) -> Response:
    await bot_handler.init_route(request['valid_data'], request=request)
    return success()
