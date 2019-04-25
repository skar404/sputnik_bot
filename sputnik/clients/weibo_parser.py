import base64
import json
import re
import time
import random
import binascii
from dataclasses import dataclass
from http.cookies import SimpleCookie

import aiohttp
import async_timeout
import rsa
from aiohttp import ContentTypeError, ClientSession
from marshmallow.compat import urlparse

from sputnik.clients.anti_captcha import AntiCaptchaService
from sputnik.clients.base import BaseClient, RequestData


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

    cookies: SimpleCookie = None


class WeiboParserClient(BaseClient):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
    }

    def __init__(self):
        self.cookies = None
        self.weibo_auth = None

    async def __aenter__(self):
        # self.jar = aiohttp.CookieJar(unsafe=True)
        self.aiohttp_session: ClientSession = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=self.VERIFY_SSL),
            cookie_jar=aiohttp.CookieJar(unsafe=True))

        await self.set_base_cookies()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aiohttp_session.close()

        return

    async def set_base_cookies(self):
        async with self.aiohttp_session.get("http://weibo.com/login.php", headers=self.HEADERS) as response:
            self.cookies = response.cookies
            self.aiohttp_session.cookie_jar.update_cookies(response.cookies)

    async def _request(self, *args, **kwargs) -> RequestData:
        req = RequestData()

        if self.cookies is not None:
            kwargs['cookies'] = self.cookies

        with async_timeout.timeout(self.TIMEOUT):
            async with self.aiohttp_session.request(*args, **kwargs) as response:
                if response.cookies:
                    self.cookies.update(response.cookies)

                req.code = response.status
                req.text = await response.text()

                try:
                    req.json = await response.json()
                except ContentTypeError:
                    req.json = {}

                req.headers = response.headers
                req.request_info = response.request_info
                req.cookies = response.cookies

        return req

    async def download_captcha(self, captcha_url):
        async with self.aiohttp_session.get(url=captcha_url, cookies=self.cookies) as response:
            if response.cookies:
                self.cookies.update(response.cookies)

            captcha_image = await response.read()

        captcha_data = base64.b64encode(captcha_image)
        return captcha_data

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

    async def create_new_post(self, message: str, photo_id: str):
        create_post_url = 'https://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd={}'.format(int(random.random() * 100000000))

        data = {
            'location': 'v6_content_home',
            'text': message,
            'appkey': '',
            'style_type': '1',
            'pic_id': photo_id,
            'tid': '',
            'pdetail': '',
            'mid': '',
            'isReEdit': 'false',
            'rank': '0',
            'rankid': '',
            'module': 'stissue',
            'pub_source': 'main_',
            'pub_type': 'dialog',
            'isPri': '0',
            '_t': '0',
        }

        ret = await self.post(
            create_post_url, data=data, headers={
                'User-Agent': ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                               "(KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"),
                'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9'
                           ',image/webp,*/*;q=0.8'),
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Referer': 'http://weibo.com'
            }
        )
        return ret

    async def push_image(self, image_raw, nick):
        params = {
            'cb': 'https://www.weibo.com/aj/static/upimgback.html?_wv=5&callback=STK_ijax_{}'.format(
                int(random.random() * 100000000)),
            'mime': 'image/jpeg',
            'data': 'base64',
            'url': 'weibo.com/u/{}'.format(nick),
            'markpos': '1',
            'logo': '1',
            # копирайт который будет воткнут на фото
            'nick': '@{}'.format(nick),
            'marks': '0',
            'app': 'miniblog',
            's': 'rdxt',
            'pri': 'null',
            'file_source': '1'
        }

        ret = await self.post(url='https://picupload.weibo.com/interface/pic_upload.php', params=params,
                              data={
                                  'b64_data': image_raw
                              })
        return ret


class WeiboParserService(WeiboParserClient):
    VERIFY_SSL = False

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
        captcha_url = "http://login.sina.com.cn/cgi/pin.php?r={}&s=0&p={}" \
            .format(int(random.random() * 100000000), weibo_auth.pc_id)
        return captcha_url

    async def check_user_is_login(self, weibo_ajax_login_url):
        req = await self.get(weibo_ajax_login_url, headers=self.HEADERS)

        uuid_res = re.findall(r'"uniqueid":"(.*?)"', req.text, re.S)
        if not uuid_res:
            return False
        else:
            return True

    async def login_user(self, login, password):
        weibo_auth = await self.get_server_data_in_login(login)
        weibo_auth.password = password

        await self.update_auth_data_set_password_secret(weibo_auth)

        captcha_text = None

        if weibo_auth.show_pin != 0:
            captcha_url = await self.get_captcha_url(weibo_auth)
            captcha_data = await self.download_captcha(captcha_url)

            captcha_text = await AntiCaptchaService().get_recaptcha_in_url(captcha_data, download_captcha=False)

        req = await self.login_user_in_captcha(weibo_auth, captcha=captcha_text)
        weibo_ajax_login_url = re.findall(r'location\.replace\([\'"](.*?)[\'"]\)', req.text)[0]

        is_login = await self.check_user_is_login(weibo_ajax_login_url)

        weibo_auth.cookies = self.cookies
        self.weibo_auth = weibo_auth

        return is_login

    async def create_post(self, message, photo_id=None):
        if photo_id is None:
            photo_id = ''
        await self.create_new_post(message, photo_id)

    async def get_id_and_push_image(self, image_raw, nick):
        req = await self.push_image(image_raw, nick)
        return req.request_info.url.query.get('pid')
