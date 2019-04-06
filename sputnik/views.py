from aiohttp.web_request import Request
from aiohttp.web_response import Response

from sputnik.bot.views import bot_handler
from sputnik.clients.telegram.schema import WebHookMessageSchema
from sputnik.shortcuts.validation import validation_shame
from sputnik.shortcuts.view import success


async def ping(_request):
    return success('pong')


@validation_shame(WebHookMessageSchema)
async def bot(request: Request) -> Response:
    await bot_handler.init_route(request['valid_data'], request=request)
    return success()
