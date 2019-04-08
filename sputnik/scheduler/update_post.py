from sputnik.clients.sputnik import SputnikService
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.models.post import PostModel
from sputnik.settings import POST_USER


async def send_message(post):
    for user_id in POST_USER:
        if post.short_link is None:
            return
        await TelegramSDK().send_message(chat_id=user_id, message=f'**Запостить новость:**\n\n{post.enclosure}')
        await TelegramSDK().send_message(
            chat_id=user_id,
            message=f'【{post.title}】\n{post.description}\n{post.short_link}',
            eply_markup={
                'inline_keyboard': [[
                    {"text": "Запостить", "callback_data": f'post_message:id:{post.id}'},
                ]]
            }
        )


async def update_post(app):
    post_list = await SputnikService().get_post(with_link=False)

    for post in post_list:
        post_req: PostModel = await PostModel.query.where(PostModel.guid == post.guid).gino.first()

        if post_req is None:
            await PostModel.create(
                guid=post.guid,

                category=post.category,
                description=post.description,
                enclosure=post.enclosure,
                link=post.link,
                post_id=post.post_id,
                pub_date=post.pub_date,
                short_link=post.short_link,
                text=post.text,
                title=post.title,
            )

        if post_req is not None:
            await send_message(post_req)
