from sputnik.clients.sputnik import SputnikService
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.models.post import PostModel
from sputnik.settings import POST_USER


async def update_post(app):
    post_list = await SputnikService().get_post(with_link=False)

    for post in post_list:
        post_req: PostModel = await PostModel.query.where(PostModel.guid == post.guid).gino.first()

        if post_req is None:
            if post.short_link is None:
                short_link = await SputnikService().get_short_link(post.post_id[8:])
                await post_req.update(short_link=short_link).apply()

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
