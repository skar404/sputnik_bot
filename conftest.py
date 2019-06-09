import sys
import pytest

from sputnik.main import init_app


sys.dont_write_bytecode = True


@pytest.fixture
def cli(loop, aiohttp_client):
    app = init_app('text', api=True)

    return loop.run_until_complete(aiohttp_client(app))
