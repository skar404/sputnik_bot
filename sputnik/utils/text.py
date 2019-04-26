from sputnik.models.post import PostModel


def get_post_text(post: PostModel):
    text = f"【{post.title}】" \
        f"{post.description} " \
        f"{post.short_link}"
    return text
