from sputnik.clients.base import BaseClient
from sputnik.settings import BITLY_ACCESS_TOKEN


class BitlyClint(BaseClient):
    BASE_URL = 'https://api-ssl.bitly.com/v3/'

    VERIFY_SSL = False

    shorten_url = 'shorten'

    async def create_short_link(self, long_url):
        data = await self.get(self._get_url('shorten_url'), params={
            'longUrl': long_url,
            'access_token': BITLY_ACCESS_TOKEN
        })
        return data.json.get('data', {})
