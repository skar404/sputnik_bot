from sputnik.models.post import PostModel


def get_post_text(post: PostModel) -> str:
    text = f"【{post.title}】" \
        f"{post.description} " \
        f"{post.short_link}"
    return text


def get_lightning_text(post: PostModel) -> str:
    text = f'快讯：{post.title} {post.short_link}'
    return text


def markdown_shielding(text: str) -> str:
    return text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
