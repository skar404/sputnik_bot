import base64

import aiohttp
import async_timeout

from sputnik.utils.text import is_valid_post


async def download_img(link, timeout=10):
    if is_valid_post(link) is False:
        return None

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
        with async_timeout.timeout(timeout):
            async with session.get(url=link) as response:
                raw_image = await response.read()

    image_base64 = base64.b64encode(raw_image)
    return image_base64
