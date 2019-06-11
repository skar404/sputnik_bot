from sputnik.models.post import PostModel


IMAGE_TYPE = ('jpg', 'png')


def get_default_post_text(post: PostModel) -> str:
    text = f"【{post.title}】" \
        f"{post.description} " \
        f"{post.short_link}"
    return text


def get_lightning_text(post: PostModel) -> str:
    text = f'快讯：{post.title} {post.short_link}'
    return text


def is_lightning(post: PostModel):
    return True if post.title == post.description else False


def get_post_text(post: PostModel) -> str:
    """
    Отдает текст поста в зависемости от новости
    :param post:
    :return:
    """
    if is_lightning(post):
        return get_lightning_text(post)
    return get_default_post_text(post)


def markdown_shielding(text: str) -> str:
    return text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")


def is_valid_post(img_url):
    if img_url is None and img_url[-3:] not in IMAGE_TYPE:
        return False
    return True
