import base64

import aiohttp


async def download_img(img_url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
        async with session.get(url=img_url) as response:
            raw_image = await response.read()

    image_base64 = base64.b64encode(raw_image)
    return image_base64
