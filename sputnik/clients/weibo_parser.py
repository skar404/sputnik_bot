import base64
import json
import time

from sputnik.clients.base import BaseClient


class WeiboParserClient(BaseClient):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
    }

    async def get_server_data(self, login_base64):
        data = await self.get("http://login.sina.com.cn/sso/prelogin.php", params={
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': login_base64,
            'rsakt': 'mod',
            'checkpin': 1,
            'client': 'ssologin.js(v1.4.18)',
            'pre_url': int(time.time() * 1000),
        }, headers=self.HEADERS)

        return data


class WeiboParserService(WeiboParserClient):

    async def get_server_data_in_login(self, username: str):
        username_base64 = base64.b64encode(username.encode("utf-8")).decode()

        req = await self.get_server_data(username_base64)

        return json.loads(req.text.replace("sinaSSOController.preloginCallBack", '').replace('(', '').replace(')', ''))
