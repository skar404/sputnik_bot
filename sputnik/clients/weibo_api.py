import urllib.parse

from sputnik import settings
from sputnik.clients.base import BaseClient


def get_authorize_link(state):
    url = 'https://api.weibo.com/oauth2/authorize?'

    return url + urllib.parse.urlencode({
        'client_id': settings.WEIBO_APP_KEY,
        'redirect_uri': settings.WEIBO_APP_HOST,
        'restype': 'code',
        'state': state
    })


class WeiboClient(BaseClient):
    BASE_URL = 'https://api.weibo.com/'

    VERIFY_SSL = False

    oauth2_url = 'oauth2/access_token'

    async def oauth_user(self, code):
        req = await self.post(self._get_url('oauth2_url'), data={
            'client_id': settings.WEIBO_APP_KEY,
            'client_secret': settings.WEIBO_APP_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.WEIBO_APP_HOST,
            'code': code,
        })
        return req


class WeiboService(WeiboClient):
    pass
