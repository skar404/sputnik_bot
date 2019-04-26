from sputnik.models.post import PostModel


def get_post_text(post: PostModel):
    text = f"【{post.title}】\n" \
        f"{post.description}\n" \
        f"{post.short_link}"
    return text
