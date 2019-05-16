from asynctest import patch

from sputnik.clients.base import RequestData
from sputnik.clients.bitly import BitlyClint


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData(
    json={'status_code': 200, 'status_txt': 'OK',
          'data': {'url': 'http://bit.ly/2JrY02X', 'hash': '2JrY02X', 'global_hash': '2JrY0jt',
                   'long_url': 'http://google.com/link/', 'new_hash': 1}},
    text='{"status_code":200,"status_txt":"OK","data":{"url":"http://bit.ly/2JrY02X","hash":"2JrY02X","global_hash":"2JrY0jt","long_url":"http://google.com/link/","new_hash":1}}',
    code=200))
async def test_create_short_link(_request_mock):
    short_link = await BitlyClint().create_short_link(f'http://google.com/link/')
    assert short_link['url'] == 'http://bit.ly/2JrY02X'
