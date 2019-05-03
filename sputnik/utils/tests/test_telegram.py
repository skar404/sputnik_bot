from sputnik.utils.telegram import get_secret_callback


def test_get_secret_callback():
    callback = get_secret_callback('send_post')
    assert callback == 'secret:dev:send_post'
