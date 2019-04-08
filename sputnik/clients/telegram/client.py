from sputnik.clients.base import BaseClient
from sputnik.settings import BOT_TOKEN, BOT_WEB_HOOK


class ParseMode:
    MARKDOWN = 'Markdown'
    HTML = 'HTML'


class TelegramClient(BaseClient):
    BASE_URL = 'https://api.telegram.org/bot{bot_token}/'.format(bot_token=BOT_TOKEN)

    VERIFY_SSL = False

    async def update_web_hook(self):
        req = await self.post(url=self._get_url('setWebhook?url={url_web_hook}', url_web_hook=BOT_WEB_HOOK))

        return req

    async def send_message(self, chat_id: str, message: str, parse_mode: ParseMode = ParseMode.MARKDOWN,
                           eply_markup=None):

        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode,
        }
        if eply_markup:
            params.update({'reply_markup': eply_markup})

        req = await self.post(
            url=self._get_url('sendMessage'),
            json=params
        )
        return req

    async def delete_message(self, chat_id: str, message_id: int):
        req = await self.post(
            url=self._get_url('deleteMessage'),
            params={
                'chat_id': chat_id,
                'message_id': message_id,
            }
        )
        return req


class TelegramSDK(TelegramClient):
    """
    Тут логика валидации входных и отдаваемый данных
    """
    pass
