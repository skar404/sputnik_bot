import async_timeout


class BaseClient:
    TIMEOUT: int = 10
    BASE_URL: str = None

    def _get_url(self, url: str, **kwargs):
        return self.BASE_URL + url.format(**kwargs)

    async def get(self, *args, **kwargs):
        return await self._request('GET', *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self._request('POST', *args, **kwargs)

    async def _request(self, *args, **kwargs):
        # from sputnik import pass
        application = object()

        with async_timeout.timeout(self.TIMEOUT):
            async with application.aiohttp_session.request(*args, **kwargs) as response:
                req = await response.json()

            return req
