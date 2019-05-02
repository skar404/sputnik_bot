# from sputnik.models.post import PostModel
# from sputnik.utils.text import get_post_text, markdown_shielding
#
#
# def test_get_post_text():
#     post = PostModel()
#     post.title = 'title'
#     post.description = 'description'
#     post.short_link = 'https://short_link.ru'
#     post_text = get_post_text(post)
#
#     assert post_text == '【title】description https://short_link.ru'
#
#
# def test_markdown_shielding():
#     text = markdown_shielding(
#         "**asterisks** or __underscores__ \n"
#         "[I'm an inline-style link](https://www.google.com) "
#         "```python\n"
#         "s = 'Python syntax highlighting'\n"
#         "print(s)"
#         "\n```")
#     assert text == """\\*\\*asterisks\\*\\* or \\_\\_underscores\\_\\_
# \\[I\'m an inline-style link](https://www.google.com) \\`\\`\\`python
# s = \'Python syntax highlighting\'
# print(s)
# \\`\\`\\`"""
