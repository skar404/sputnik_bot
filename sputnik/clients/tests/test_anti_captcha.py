from asynctest import patch, call

from sputnik.clients.anti_captcha import AntiCaptchaService
from sputnik.clients.base import RequestData
from sputnik.settings import ANTI_CAPTCHA_KEY


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_crete_captcha_task(mock_request):
    await AntiCaptchaService().crete_captcha_task(b'base64 image test')

    assert mock_request.await_args == call(
        'POST',
        json={'clientKey': ANTI_CAPTCHA_KEY,
              'task': {'type': 'ImageToTextTask', 'body': 'base64 image test', 'phrase': False, 'case': False,
                       'math': 0, 'minLength': 0, 'maxLength': 0}},
        url='https://api.anti-captcha.com/createTask'
    )


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_get_task(mock_request):
    await AntiCaptchaService().get_task('task-id-1')

    assert mock_request.await_args == call(
        'POST',
        'https://api.anti-captcha.com/getTaskResult',
        json={'clientKey': ANTI_CAPTCHA_KEY,
              'taskId': 'task-id-1'})


@patch('sputnik.clients.anti_captcha.AntiCaptchaClient.get_task', return_value=RequestData(json={
    'status': 'ready',
    'solution': {
        'text': 'вацфц'
    }
}))
@patch('sputnik.clients.anti_captcha.AntiCaptchaClient.crete_captcha_task', return_value=RequestData(json={
    'taskId': 10
}))
@patch('sputnik.clients.anti_captcha.download_img', return_value=b'base64 image test')
async def test_get_recaptcha_in_url(mock_download_img, mock_crete_captcha_task, mock_get_task):
    captcha_text = await AntiCaptchaService().get_recaptcha_in_url('http://kate.jpg', download_captcha=True)

    assert captcha_text == 'вацфц'

    assert mock_download_img.await_args == call('http://kate.jpg', 10)
    assert mock_crete_captcha_task.await_args == call(b'base64 image test')
    assert mock_get_task.await_args == call(10)
