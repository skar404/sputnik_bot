from aiohttp.web_request import Request
from aiohttp.web_response import Response

from sputnik.bot.views import bot_handler
from sputnik.clients.telegram.schema import WebHookMessageSchema
from sputnik.models.main import DataBase, PostModel
from sputnik.schemas.post import PostResponse, PostStatus
from sputnik.shortcuts.validation import validation_shame
from sputnik.shortcuts.view import success


async def ping(_request: Request) -> Response:
    await DataBase.scalar('SELECT 1;')
    return success('pong')


async def get_all_post(_request: Request) -> Response:
    post_list = await PostModel.filter()
    return success([
        PostResponse(
            id=post.id,
            link=post.link,
            short_link=post.short_link,

            photo=post.enclosure,

            title=post.title,
            text=post.description,

            created_at=post.created_at.timestamp(),
            status=PostStatus(
                is_send_telegram=post.status_send_tg,
                is_send_weibo=post.status_posted
            ).__dict__
        ).__dict__
        for post in post_list
    ])


@validation_shame(WebHookMessageSchema)
async def bot(request: Request) -> Response:
    await bot_handler.init_route(request['valid_data'], request=request)
    return success()
