from typing import List

from sputnik.clients.telegram.client import TelegramSDK
from sputnik.models.post import PostModel
from sputnik.settings import POST_USER
from sputnik.utils.short_link import get_short_link
from sputnik.utils.telegram import get_start_post_reply_markup
from sputnik.utils.text import markdown_shielding, get_post_text, is_lightning


async def send_message(post: PostModel):
    for user_id in POST_USER:
        if post.short_link is None:
            short_link = await get_short_link(post.post_id, post.guid)
            await post.update(short_link=short_link).apply()

        tags_list = {'#post', f'#id\\_{post.id}'}
        if is_lightning(post):
            tags_list.add('#lightning')
        text_raw = get_post_text(post)

        # replace is mix markdown
        weibo_text = markdown_shielding(text_raw)

        message = '{weibo_text} \n\nполная ссылка: {guid}\n\nтеги: {tags}'.format(
            weibo_text=weibo_text, guid=markdown_shielding(post.guid), tags=' '.join(tags_list)
        )

        kwarg = {
            'chat_id': user_id,
            'message': message,
            'reply_markup': get_start_post_reply_markup(url=post.guid, post_id=post.id)
        }

        method_send = TelegramSDK().send_message
        if post.enclosure is not None and post.enclosure[-3:].lower() in ('jpg', 'png'):
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


async def send_new_post():
    posts_list: List[PostModel] = await PostModel.query \
        .where(PostModel.status_send_tg.isnot(True)) \
        .gino.all()

    for post in posts_list:
        await send_message(post)
