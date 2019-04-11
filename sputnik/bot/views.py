import logging

import jwt

from sputnik.clients.telegram.client import TelegramSDK
from sputnik.bot.router import TelegramRouter
from sputnik.clients.weibo_api import get_authorize_link
from sputnik.models.post import PostModel
from sputnik.settings import BOT_TOKEN, JWT_SECRET
from sputnik.shortcuts.main import users_info

bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


class RabbitMessageType:
    SEND_SONG_LIST = 'SEND_SONG_LIST'
    DOWNLOAD_SONG = 'DOWNLOAD_SONG'


@bot_handler.command(command='start')
@users_info
async def command_start(message, _request):
    text = 'Привет @{user_name},\n' \
        'Просто отправь мне имя артиста и/или название композиции,\n' \
        'и я найду эту песню для тебя!'.format(user_name=message['message']['from']['username'])

    await TelegramSDK() \
        .send_message(chat_id=message['message']['chat']['id'], message=text)


@bot_handler.command(command='help')
@users_info
async def command_help(message, _request):
    text = 'Привет @{user_name},\n' \
        'У меня есть несколько фишечек, допустим:\n' \
        ' - вы не нашли трек тогда можете ввести названив в кавычках "моя песня" и \n'\
        'поишим по всей нашей базе : )'.format(user_name=message['message']['from']['username'])

    await TelegramSDK() \
        .send_message(chat_id=message['message']['chat']['id'], message=text)


@bot_handler.command(command='weibo')
@users_info
async def login_weibo(message, _request):
    chat_id = message['message']['chat']['id']

    state = jwt.encode({'chat_id': chat_id}, JWT_SECRET)
    text = 'Для входа в Weibo перейдите по ссылки: [ввойти в waibo]({})'.format(get_authorize_link(state=state))

    await TelegramSDK() \
        .send_message(chat_id=chat_id, message=text)


@bot_handler.callback_query(callback_key='post_message:id')
@users_info
async def callback_send_post(message, _request):
    try:
        post_id = int(message['callback_query']['data'].split(':')[-1])
    except ValueError:
        logging.warning('value error')
        return

    post_req: PostModel = await PostModel.query.where(PostModel.id == post_id).gino.first()
