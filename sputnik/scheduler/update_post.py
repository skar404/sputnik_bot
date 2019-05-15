from sputnik.clients.sputnik import SputnikService
from sputnik.models.post import PostModel
from sputnik.utils.short_link import get_short_link


async def update_post():
    post_list = await SputnikService().get_post(with_link=True)

    for post in post_list:
        post_req: PostModel = await PostModel.query.where(PostModel.guid == post.guid).gino.first()
        kwargs = {
            'category': post.category,
            'description': post.description,
            'enclosure': post.enclosure,
            'link': post.link,
            'post_id': post.post_id,
            'pub_date': post.pub_date,
            'short_link': post.short_link,
            'text': post.text,
            'title': post.title,
        }

        if post_req is None:
            if post.short_link is None:
                kwargs['short_link'] = await get_short_link(post.post_id, post.guid)

            kwargs['guid'] = post.guid

            await PostModel.create(**kwargs)
        else:
            if post_req.short_link is None:
                kwargs['short_link'] = await get_short_link(post.post_id, post.guid)

            if post_req.enclosure is None:
                await post_req.update(**kwargs).apply()
