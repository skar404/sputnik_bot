from dataclasses import dataclass

import aiohttp
import async_timeout
from typing import Optional

from aiohttp import ContentTypeError


@dataclass
class RequestData:
    json: Optional[dict] = None
    text: str = None
    code: int = None


class BaseClient:
    TIMEOUT: int = 10
    BASE_URL: str = None

    def _get_url(self, url: str, **kwargs):
        return self.BASE_URL + url.format(**kwargs)

    async def get(self, *args, **kwargs) -> RequestData:
        return await self._request('GET', *args, **kwargs)

    async def post(self, *args, **kwargs) -> RequestData:
        return await self._request('POST', *args, **kwargs)

    async def _request(self, *args, **kwargs) -> RequestData:
        req = RequestData()

        with async_timeout.timeout(self.TIMEOUT):
            async with aiohttp.ClientSession() as session:
                async with session.request(*args, **kwargs) as response:
                    req.code = response.status
                    req.text = await response.text()

                    try:
                        req.json = await response.json()
                    except ContentTypeError:
                        req.json = {}

        return req
