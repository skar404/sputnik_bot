from http.cookies import SimpleCookie

from asynctest import patch

from sputnik.clients.base import RequestData
from sputnik.clients.weibo_parser import WeiboParserService, cookies_to_dict, WeiboAuthData

COOKIE_DICT = {
    'login_sid_t': '3e028aef97ffe0e74408712f2cc17086',
    'cross_origin_proto': 'SSL',
    'Ugrow-G0': 'ea90f703b7694b74b62d38420b5273df'
}
COOKIE = SimpleCookie()
COOKIE.load(COOKIE_DICT)

WEIBO_AUTH = WeiboAuthData(
    username_base64='dGVzdF91c2Vy',
    ret_code=0,
    server_time=1557787376,
    pc_id='gz-402990f69084adbcd56ffb7155d4e7de32d6', nonce='01PJE9',
    pubkey='EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443',
    rsakv='1330428213', is_open_lock=0,
    show_pin=0,
    exec_time=21,
    password='test',
    password_secret=b'7ef1cd3221ce3ae4778d18e5551e3613239ec1045ee14bb1876074344409d6705e8ffe6e116e4516cbc562ed187b1d3c1927720a1002a2329b1451777230412316039d98bfd671cd2c65d05ca98f52a6b4579e2e3c3d2970e8ddfde8824caec1c2f0707d8045d93ed96ff90dbc7f9c3006b40f79bee4abbadf9dc7621a701abb',
    cookies=COOKIE
)


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


@patch('sputnik.clients.weibo_parser.WeiboParserClient._request', return_value=RequestData())
async def test_get_server_data(_request_mock):
    data = await WeiboParserService(cookies=COOKIE, weibo_auth=WEIBO_AUTH) \
        .get_server_data(WEIBO_AUTH.username_base64)

    assert data == RequestData()


@patch('sputnik.clients.weibo_parser.WeiboParserService._request', return_value=RequestData())
async def test_login_user_in_captcha(_request_mock):
    data = await WeiboParserService(cookies=COOKIE, weibo_auth=WEIBO_AUTH) \
        .login_user_in_captcha(WEIBO_AUTH, captcha='1234')

    assert data == RequestData()


@patch('sputnik.clients.weibo_parser.WeiboParserService._request', return_value=RequestData())
async def test_create_new_post(_request_mock):
    data = await WeiboParserService(cookies=COOKIE, weibo_auth=WEIBO_AUTH) \
        .create_new_post(message='test', photo_id='10')

    assert data == RequestData()


@patch('sputnik.clients.weibo_parser.WeiboParserService._request', return_value=RequestData())
async def test_push_image(_request_mock):
    data = await WeiboParserService(cookies=COOKIE, weibo_auth=WEIBO_AUTH) \
        .push_image(image_raw='test', nick='@test')

    assert data == RequestData()
