import base64
import json
import time
import random
import binascii
from dataclasses import dataclass

import rsa

from sputnik.clients.anti_captcha import AntiCaptchaService
from sputnik.clients.base import BaseClient


@dataclass
class WeiboAuthData:
    username_base64: int
    ret_code: int
    server_time: int
    pc_id: str
    nonce: str
    pubkey: str
    rsakv: str
    is_open_lock: int
    sms_url: str
    show_pin: int
    exec_time: int

    password: str = None
    password_secret: bytes = None


class WeiboParserClient(BaseClient):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
    }

    async def get_server_data(self, login_base64):
        ret = await self.get("http://login.sina.com.cn/sso/prelogin.php", params={
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': login_base64,
            'rsakt': 'mod',
            'checkpin': 1,
            'client': 'ssologin.js(v1.4.18)',
            'pre_url': int(time.time() * 1000),
        }, headers=self.HEADERS)

        return ret

    async def login_user_in_captcha(self, weibo_auth: WeiboAuthData, captcha=None):
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

        data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
            'vsnf': '1',
            'su': weibo_auth.username_base64,
            'service': 'miniblog',
            'servertime': weibo_auth.server_time,
            'nonce': weibo_auth.nonce,
            'pwencode': 'rsa2',
            'rsakv': weibo_auth.rsakv,
            'sp': weibo_auth.password_secret.decode("utf-8"),
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        if captcha is not None:
            data['door'] = captcha

        ret = await self.post(login_url, data=data, headers=self.HEADERS)
        return ret


class WeiboParserService(WeiboParserClient):

    async def get_server_data_in_login(self, username: str) -> WeiboAuthData:
        username_base64 = base64.b64encode(username.encode("utf-8")).decode()

        req = await self.get_server_data(username_base64)

        res = json.loads(req.text.replace("sinaSSOController.preloginCallBack", '').replace('(', '').replace(')', ''))
        return WeiboAuthData(
            username_base64=username_base64,
            ret_code=res.get('retcode'),
            server_time=res.get('servertime'),
            pc_id=res.get('pcid'),
            nonce=res.get('nonce'),
            pubkey=res.get('pubkey'),
            rsakv=res.get('rsakv'),
            is_open_lock=res.get('is_openlock'),
            sms_url=res.get('smsurl'),
            show_pin=res.get('showpin'),
            exec_time=res.get('exectime'),
        )

    async def get_password_secret(self, weibo_auth: WeiboAuthData) -> bytes:
        rsa_public_key = int(weibo_auth.pubkey, 16)
        key = rsa.PublicKey(rsa_public_key, 65537)

        message = f'{weibo_auth.server_time}\t{weibo_auth.nonce}\n{weibo_auth.password}'.encode("utf-8")
        password_key = rsa.encrypt(message, key)
        password_key = binascii.b2a_hex(password_key)
        return password_key

    async def update_auth_data_set_password_secret(self, weibo_auth: WeiboAuthData):
        weibo_auth.password_secret = await self.get_password_secret(weibo_auth)

    async def get_captcha_url(self, weibo_auth: WeiboAuthData):
        captcha_url = f"http://login.sina.com.cn/cgi/pin.php?r={int(random.random() * 100000000)}&s=0&p={weibo_auth.pc_id}"
        return captcha_url

    async def login_user(self, weibo_auth: WeiboAuthData):
        captcha_text = None

        if weibo_auth.show_pin != 0:
            captcha_url = await self.get_captcha_url(weibo_auth)
            captcha_text = await AntiCaptchaService().get_recaptcha_in_url(captcha_url)

        req = await self.login_user_in_captcha(weibo_auth, captcha=captcha_text)
        return req
