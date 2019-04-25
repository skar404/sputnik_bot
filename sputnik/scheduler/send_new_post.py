from sqlalchemy import true
from typing import List

from sputnik.clients.sputnik import SputnikService
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.models.post import PostModel
from sputnik.settings import POST_USER


async def send_message(post: PostModel):
    for user_id in POST_USER:
        if post.short_link is None:
            short_link = await SputnikService().get_short_link(post.post_id[8:])
            await post.update(short_link=short_link).apply()

        await TelegramSDK().send_message(chat_id=user_id, message=f'**Запостить новость:**\n\n{post.enclosure}')
        await TelegramSDK().send_message(
            chat_id=user_id,
            message=f'【{post.title}】\n{post.description}\n{post.short_link}',
            reply_markup={
                'inline_keyboard': [[
                    {"text": "Запостить", "callback_data": f'post_message:id:{post.id}'},
                ]]
            }
        )
        await post.update(status_send_tg=True).apply()


async def send_new_post(app):
    posts_list: List[PostModel] = await PostModel.query.where(PostModel.status_send_tg.isnot(True)).gino.all()

    for post in posts_list:
        await send_message(post)
