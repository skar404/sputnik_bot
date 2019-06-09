from sputnik.clients.bitly import BitlyClint


async def get_short_link(post_id: str, full_link: str):
    from sputnik.clients.sputnik import SputnikService, SputnikClintError

    short_link = None
    try:
        short_link = await SputnikService().get_short_link(post_id[8:])
    except SputnikClintError:
        short_link_bitly = await BitlyClint().create_short_link(full_link)
        if short_link_bitly:
            short_link = short_link_bitly.get('url') if short_link_bitly.get('url') else None

    short_link_bitly = await BitlyClint().create_short_link(full_link)
    if short_link_bitly:
        short_link = short_link_bitly.get('url') if short_link_bitly.get('url') else None

    if not short_link:
        short_link = full_link

    return short_link
