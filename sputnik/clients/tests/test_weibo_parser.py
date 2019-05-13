from http.cookies import SimpleCookie

from asynctest import patch

from sputnik.clients.weibo_parser import WeiboParserService, cookies_to_dict, WeiboAuthData

COOKIE_DICT = {
    'login_sid_t': '3e028aef97ffe0e74408712f2cc17086',
    'cross_origin_proto': 'SSL',
    'Ugrow-G0': 'ea90f703b7694b74b62d38420b5273df'
}
COOKIE = SimpleCookie()
COOKIE.load(COOKIE_DICT)


def test_cookies_to_dict():
    cookie = SimpleCookie()
    cookie.load(COOKIE_DICT)

    cookie_dict = cookies_to_dict(cookie)

    assert cookie_dict == COOKIE_DICT


async def test_weibo_cline():
    async with WeiboParserService() as weibo_service:
        weibo_auth = await weibo_service.get_server_data_in_login(username='test_user')

        assert type(weibo_auth) == WeiboAuthData
        assert weibo_auth.username_base64 == 'dGVzdF91c2Vy'


@patch('sputnik.clients.weibo_parser.WeiboParserService.get_base_cookies', return_value=COOKIE)
async def test_weibo_parser_client_with(_cookie_mock):
    async with WeiboParserService() as weibo_service:
        assert COOKIE == weibo_service.cookies
