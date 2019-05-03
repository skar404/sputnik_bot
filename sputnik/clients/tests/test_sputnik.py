from asynctest import patch

from sputnik.clients.base import RequestData


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_get_post_data():
    pass
