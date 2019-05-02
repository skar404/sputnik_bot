# from sputnik.models.post import PostModel
#
#
# def get_post_text(post: PostModel) -> str:
#     text = f"【{post.title}】" \
#         f"{post.description} " \
#         f"{post.short_link}"
#     return text
#
#
# def markdown_shielding(text: str) -> str:
#     return text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
