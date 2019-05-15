from sputnik.clients.bitly import BitlyClint


async def get_short_link(post_id: str, full_link: str):
    from sputnik.clients.sputnik import SputnikService, SputnikClintError

    try:
        short_link = await SputnikService().get_short_link(post_id[8:])
    except SputnikClintError:
        short_link = await BitlyClint().create_short_link(full_link)
    return short_link
