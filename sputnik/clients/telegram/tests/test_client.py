from asynctest import patch, call

from sputnik.clients.base import RequestData
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.settings import BOT_WEB_HOOK, BOT_TOKEN

TEST_TELEGRAM_URL = 'https://api.telegram.org/bot{token}/'.format(token=BOT_TOKEN)


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_update_web_hook(mock_request):
    await TelegramSDK().update_web_hook()

    assert mock_request.await_args == call(
        'POST',
        url=TEST_TELEGRAM_URL + 'setWebhook?url={web_hook_url}'.format(
            web_hook_url=BOT_WEB_HOOK,
        ))


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_send_photo(mock_request):
    await TelegramSDK().send_photo(
        chat_id='1',
        photo='http://image.png',
        message='Hello world',
        reply_markup={
            'inline_keyboard': [[
                {"text": "тестовая ссылка", "url": 'http://localhost'},
            ]]
        },
        reply_to_message_id=10
    )
    assert mock_request.await_args == call(
        'POST',
        json={'chat_id': '1', 'caption': 'Hello world', 'parse_mode': 'Markdown',
              'photo': 'http://image.png',
              'reply_markup': {'inline_keyboard': [
                  [{'text': 'тестовая ссылка', 'url': 'http://localhost'}]]},
              'reply_to_message_id': 10},
        url=TEST_TELEGRAM_URL + 'sendPhoto'
    )


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_send_message(mock_request):
    await TelegramSDK().send_message(
        chat_id='1',
        message='Hello world',
        reply_markup={
            'inline_keyboard': [[
                {"text": "тестовая ссылка", "url": 'http://localhost'},
            ]]
        },
        reply_to_message_id=10
    )
    assert mock_request.await_args == call(
        'POST',
        json={'chat_id': '1',
              'text': 'Hello world',
              'parse_mode': 'Markdown',
              'reply_markup': {'inline_keyboard': [
                  [{'text': 'тестовая ссылка', 'url': 'http://localhost'}]]},
              'reply_to_message_id': 10},
        url=TEST_TELEGRAM_URL + 'sendMessage'
    )


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_delete_message(mock_request):
    await TelegramSDK().delete_message(
        chat_id='1',
        message_id=1
    )
    assert mock_request.await_args == call(
        'POST',
        params={'chat_id': '1', 'message_id': 1},
        url=TEST_TELEGRAM_URL + 'deleteMessage'
    )


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_edit_message(mock_request):
    await TelegramSDK().edit_message(
        chat_id='1',
        message_id=1,
        message='Hello world #2',
        reply_markup={
            'inline_keyboard': [[
                {"text": "тестовая ссылка", "url": 'http://localhost'},
            ]]
        }
    )
    assert mock_request.await_args == call(
        'POST',
        json={
            'chat_id': '1',
            'message_id': 1,
            'parse_mode': 'Markdown',
            'text': 'Hello world #2',
            'reply_markup': {'inline_keyboard': [[{'text': 'тестовая ссылка', 'url': 'http://localhost'}]]}},
        url=TEST_TELEGRAM_URL + 'editMessageText'
    )


@patch('sputnik.clients.base.BaseClient._request', return_value=RequestData())
async def test_edit_only_message_reply(mock_request):
    await TelegramSDK().edit_only_message_reply(
        chat_id='1',
        message_id=1,
        reply_markup={
            'inline_keyboard': [[
                {"text": "тестовая ссылка", "url": 'http://localhost'},
            ]]
        }
    )

    assert mock_request.await_args == call(
        'POST',
        json={
            'chat_id': '1',
            'message_id': 1,
            'reply_markup': {'inline_keyboard': [[{'text': 'тестовая ссылка', 'url': 'http://localhost'}]]}},
        url=TEST_TELEGRAM_URL + 'editMessageReplyMarkup'
    )
