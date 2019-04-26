from sputnik.clients.base import BaseClient
from sputnik.settings import BOT_TOKEN, BOT_WEB_HOOK, TG_PROXY_URL


class ParseMode:
    MARKDOWN = 'Markdown'
    HTML = 'HTML'


class TelegramClient(BaseClient):
    BASE_URL = 'https://api.telegram.org/bot{bot_token}/'.format(bot_token=BOT_TOKEN)

    VERIFY_SSL = False

    PROXY_URL = TG_PROXY_URL

    set_web_hook_url = 'setWebhook?url={url_web_hook}'
    send_message_url = 'sendMessage'
    delete_message_url = 'deleteMessage'
    edit_message_url = 'editMessageText'
    edit_message_reply_markup_url = 'editMessageReplyMarkup'

    async def update_web_hook(self):
        req = await self.post(url=self._get_url('set_web_hook_url', url_web_hook=BOT_WEB_HOOK))

        return req

    async def send_message(self, chat_id: str, message: str, parse_mode: ParseMode = ParseMode.MARKDOWN,
                           reply_markup=None, reply_to_message_id=None):
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode,
        }
        if reply_markup:
            params.update({'reply_markup': reply_markup})

        if reply_to_message_id is not None:
            params.update({'reply_to_message_id': reply_to_message_id})

        req = await self.post(
            url=self._get_url('send_message_url'),
            json=params
        )
        return req

    async def delete_message(self, chat_id: str, message_id: int):
        req = await self.post(
            url=self._get_url('delete_message_url'),
            params={
                'chat_id': chat_id,
                'message_id': message_id,
            }
        )
        return req

    async def edit_message(self, chat_id: str, message_id: int, text=None, reply_markup=None,
                           parse_mode: ParseMode = ParseMode.MARKDOWN):
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'parse_mode': parse_mode,
        }

        if text is not None:
            params.update({'text': text})

        if reply_markup is not None:
            params.update({'reply_markup': reply_markup})

        req = await self.post(
            url=self._get_url('edit_message_url'),
            json=params
        )
        return req

    async def edit_only_message_reply(self, chat_id: str, message_id: int, reply_markup=None):
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
        }

        if reply_markup is not None:
            params.update({'reply_markup': reply_markup})

        req = await self.post(
            url=self._get_url('edit_message_reply_markup_url'),
            json=params
        )
        return req


class TelegramSDK(TelegramClient):
    """
    Тут логика валидации входных и отдаваемый данных
    """
    pass
