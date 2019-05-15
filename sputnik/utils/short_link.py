from sputnik.clients.bitly import BitlyClint
from sputnik.clients.sputnik import SputnikService, SputnikClintError


async def get_short_link(post_id: str, full_link: str):
    try:
        short_link = await SputnikService().get_short_link(post_id[8:])
    except SputnikClintError:
        short_link = await BitlyClint().create_short_link(full_link)
    return short_link
