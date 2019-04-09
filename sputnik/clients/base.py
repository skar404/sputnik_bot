from dataclasses import dataclass
from typing import Optional

import aiohttp
import async_timeout

from aiohttp import ContentTypeError


@dataclass
class RequestData:
    json: Optional[dict] = None
    text: str = None
    code: int = None


class BaseClient:
    TIMEOUT: int = 10
    BASE_URL: str = None
    VERIFY_SSL: bool = True

    def _get_url(self, url_name: str, **kwargs):
        return self.BASE_URL + getattr(self, url_name).format(**kwargs)

    async def get(self, *args, **kwargs) -> RequestData:
        return await self._request('GET', *args, **kwargs)

    async def post(self, *args, **kwargs) -> RequestData:
        return await self._request('POST', *args, **kwargs)

    async def _request(self, *args, **kwargs) -> RequestData:
        req = RequestData()

        with async_timeout.timeout(self.TIMEOUT):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=self.VERIFY_SSL)) as session:
                async with session.request(*args, **kwargs) as response:
                    req.code = response.status
                    req.text = await response.text()

                    try:
                        req.json = await response.json()
                    except ContentTypeError:
                        req.json = {}

        return req
