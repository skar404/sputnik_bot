import asyncio
import base64
import logging
import time

from sputnik import settings
from sputnik.clients.base import BaseClient
from sputnik.clients.file_download import download_img
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.bot.router import TelegramRouter
from sputnik.clients.weibo_parser import WeiboParserService
from sputnik.models.main import DataBase
from sputnik.models.post import PostModel
from sputnik.settings import BOT_TOKEN
from sputnik.shortcuts.main import users_info, white_list, get_thank_message
from sputnik.utils.text import get_post_text

bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


class RabbitMessageType:
    SEND_SONG_LIST = 'SEND_SONG_LIST'
    DOWNLOAD_SONG = 'DOWNLOAD_SONG'


@bot_handler.command(command='start')
@users_info
@white_list
async def command_start(message, _request):
    user_name = message['message']['from'].get('username')

    text = f'Привет @{user_name},\n' \
        'Данный бот уже настроен и теперь ты будешь получать уведомления о всех новостях\n' \
        f'Бот обнволяет посты раз в {settings.UPDATE_POST_SECONDS} секунд и\n' \
        f'отправлет их в telegram раз в {settings.SEND_POST_SECONDS} секунд.'

    await TelegramSDK() \
        .send_message(chat_id=message['message']['chat']['id'], message=text)


@bot_handler.command(command='help')
@users_info
@white_list
async def command_help(message, _request):
    is_connect_db = False
    try:
        is_connect_db = await DataBase.scalar('SELECT true;')
    except Exception:
        pass

    text = 'Техническая информация о боте: \n\n' \
        f'Белый лист: {", ".join(settings.WHITE_LIST_USER)}\n' \
        f'Окружение: {settings.ENVIRONMENT}\n' \
        f'Число рабочих: {settings.WORKERS}\n' \
        f'Ссылка на бота: {settings.BOT_WEB_HOOK}\n' \
        f'Проверка подключения в базе данных: {is_connect_db}\n' \
        f'Время между обновлениями постов: {settings.UPDATE_POST_SECONDS}\n' \
        f'Время между отправкой постов в TG: {settings.SEND_POST_SECONDS}\n' \
           '# todo: добавить описания для /help этот метод вынести в /ping или /status'

    req = await TelegramSDK() \
        .send_message(chat_id=message['message']['chat']['id'], message=text)


async def send_message_weibo(chat_id, message_id, post_id):
    start_time = time.time()

    post: PostModel = await PostModel.query.where(PostModel.id == post_id).gino.first()
    if post.enclosure[-3:] != 'jpg':
        # TODO сказать что это не картинка и не получаться обновить
        # TODO убрать на уровне отправеки в tg
        return

    if post.status_posted is True:
        return

    await post.update(status_posted=True).apply()

    image = await download_img(post.enclosure)

    text = get_post_text(post)

    async with WeiboParserService() as weibo_service:
        await weibo_service.login_user(settings.WEIBO_LOGIN, settings.WEIBO_PASSWORD)
        photo_id = await weibo_service.get_id_and_push_image(image, settings.WEIBO_NICK)
        await weibo_service.create_post(text, photo_id)

    reply_markup = {
        'inline_keyboard': [[
            {"text": "Сообщений успешно отправленно в weibo", "url": settings.WEIBO_HOST_URL},
        ], [
            {"text": "Тест, отправит, повторно отправит", "callback_data": f'post_message:id:{post_id}'},
        ]]
    }

    await TelegramSDK().edit_only_message_reply(chat_id, message_id, reply_markup=reply_markup)

    end_time = time.time() - start_time
    await TelegramSDK().send_message(chat_id, f'Я успешно отправил в weibo, время: {end_time}', reply_to_message_id=message_id)


@bot_handler.callback_query(callback_key='post_message:id')
@users_info
@white_list
async def callback_send_post(message, _request):
    try:
        post_id = int(message['callback_query']['data'].split(':')[-1])
    except ValueError:
        logging.warning('value error')
        return

    chat_id = message['user_info']['id']
    message_id = message['callback_query']['message']['message_id']

    reply_markup = {
        'inline_keyboard': [[
            {"text": "Сообщений скоро будет отправленно в weibo", "url": settings.WEIBO_HOST_URL},
        ], [
            {"text": "Тест, отправит, повторно отправит", "callback_data": f'post_message:id:{post_id}'},
        ]]
    }

    await TelegramSDK().edit_only_message_reply(chat_id, message_id, reply_markup=reply_markup)

    asyncio.ensure_future(send_message_weibo(chat_id, message_id, post_id))


@bot_handler.text()
@users_info
@white_list
async def test_message(message, _request):
    with open('./test_data/kate.jpg', 'rb') as f:
        data = base64.b64encode(f.read()).decode()

    chat_id = message['user_info']['id']

    message_text = message['message']['text']
    message_id = message['message']['message_id']

    # todo нужно изучить способ расопзнания текста
    if 'спасиб' in message_text:
        # await TelegramSDK().send_photo(chat_id=chat_id, message="""【一只猫赶走了六条狗】在土耳其，一只猫击退了由六条狗组成的狗群，保卫了自己的领地。《每日邮报》注意到了相关视频。http://sptnkne.ws/mq9J""",
        #                                reply_to_message_id=message_id,
        #                                photo='http://cdn3.img.sputniknews.cn/images/102683/74/1026837458.jpg',
        #                                reply_markup=reply_markup
        #                                )
        await TelegramSDK().send_message(chat_id=chat_id, message=get_thank_message(), reply_to_message_id=message_id)
