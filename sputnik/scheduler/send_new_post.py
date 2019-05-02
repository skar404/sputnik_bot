from typing import List

from sputnik.clients.sputnik import SputnikService
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.models.post import PostModel
from sputnik.settings import POST_USER
from sputnik.utils.text import get_post_text, markdown_shielding


async def send_message(post: PostModel):
    for user_id in POST_USER:
        if post.short_link is None:
            short_link = await SputnikService().get_short_link(post.post_id[8:])
            await post.update(short_link=short_link).apply()

        # replace is mix markdown
        weibo_text = markdown_shielding(get_post_text(post))
        message = '**Запостить новость:**\n{weibo_text} \n\nполная ссылка: {guid}'.format(
            weibo_text=weibo_text, guid=markdown_shielding(post.guid)
        )

        kwarg = {
            'chat_id': user_id,
            'message': message,
            'reply_markup': {
                'inline_keyboard': [[
                    {"text": f"к новости", "url": post.guid},
                ], [
                    {"text": "Запостить", "callback_data": f'post_message:id:{post.id}'},
                ]]
            }
        }

        method_send = TelegramSDK().send_message
        if post.enclosure is not None and post.enclosure[-3:].lower() == 'jpg':
            kwarg.update({'photo': post.enclosure})
            method_send = TelegramSDK().send_photo

        req = await method_send(**kwarg)
        if req.code != 200:
            await TelegramSDK().send_message(
                chat_id=user_id,
                message=f'Ошибка отправки новости в Telegram:\n'
                f'id поста в базе: `{post.id}`\n'
                f'ответ telegram:\n'
                f'```\n{req.json}```,\n'
                f'**наши специалисты уже работают над проблемой**\n'
                f'#error #send\\_message #post #post\\_{post.id}'
            )

        await post.update(status_send_tg=True).apply()


async def send_new_post(app):
    posts_list: List[PostModel] = await PostModel.query.where(PostModel.status_send_tg.isnot(True)).gino.all()

    for post in posts_list:
        await send_message(post)
