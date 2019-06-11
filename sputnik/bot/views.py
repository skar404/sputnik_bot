import asyncio
import logging
import time

from sputnik import settings
from sputnik.clients.file_download import download_img
from sputnik.clients.telegram.client import TelegramSDK
from sputnik.bot.router import TelegramRouter
from sputnik.clients.weibo_parser import WeiboParserService
from sputnik.models.main import DataBase
from sputnik.models.post import PostModel
from sputnik.settings import BOT_TOKEN
from sputnik.shortcuts.main import users_info, white_list, get_thank_message
from sputnik.utils.text import get_post_text, get_lightning_text

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


@bot_handler.command(command='ping')
@users_info
@white_list
async def ping(message, _request):
    chat_id = message['user_info']['id']
    message_id = message['message']['message_id']
    await DataBase.scalar('SELECT 1;')
    await TelegramSDK().send_message(chat_id=chat_id, message='pong', reply_to_message_id=message_id)


@bot_handler.command(command='help')
@users_info
@white_list
async def command_help(message, _request):
    is_connect_db = False
    try:
        is_connect_db = await DataBase.scalar('SELECT true;')
    except Exception as ex:
        logging.exception('not connect to db ex', exc_info={
            ex: ex
        })

    text = 'Техническая информация о боте: \n\n' \
        f'Белый лист: {", ".join(settings.WHITE_LIST_USER)}\n' \
        f'Окружение: {settings.ENVIRONMENT}\n' \
        f'Число рабочих: {settings.WORKERS}\n' \
        f'Ссылка на бота: {settings.BOT_WEB_HOOK}\n' \
        f'Проверка подключения в базе данных: {is_connect_db}\n' \
        f'Время между обновлениями постов: {settings.UPDATE_POST_SECONDS}\n' \
        f'Время между отправкой постов в TG: {settings.SEND_POST_SECONDS}\n' \
        f'Версия: {settings.APP_VERSION}'

    await TelegramSDK().send_message(chat_id=message['message']['chat']['id'], message=text)


async def post_to_weibo(text, image):
    async with WeiboParserService() as weibo_service:
        await weibo_service.login_user(settings.WEIBO_LOGIN, settings.WEIBO_PASSWORD)
        if image is None:
            photo_id = await weibo_service.get_id_and_push_image(image, settings.WEIBO_NICK)
        await weibo_service.create_post(text, photo_id)


async def send_message_weibo(chat_id, message_id, post_id):
    start_time = time.time()

    post: PostModel = await PostModel.query.where(PostModel.id == post_id).gino.first()
    if post.enclosure[-3:] not in ('jpg', 'png') and post.title != post.description:
        await TelegramSDK().send_message(chat_id=chat_id,
                                         message="новость не соотвествует условию и не была отпарвленна в weibo",
                                         reply_to_message_id=message_id)
        return

    if post.status_posted is True:
        await TelegramSDK().send_message(chat_id=chat_id,
                                         message="новость уже была отправленна в weibo",
                                         reply_to_message_id=message_id)
        return

    await post.update(status_posted=True).apply()

    image = None
    if post.enclosure[-3:] not in ('jpg', 'png'):
        image = await download_img(post.enclosure)

    if post.title == post.description:
        text = get_lightning_text(post)
    else:
        text = get_post_text(post)

    # TODO хадкот чтобы в случаи падния повторно отпаравлять
    is_err = True
    for _ in range(3):
        try:
            await post_to_weibo(text, image)
            is_err = False
            break
        except Exception as ex:
            logging.exception('error send waibo', exc_info={
                ex: ex
            })

    if is_err:
        logging.exception('error send post to weibo')
        await post.update(status_posted=False).apply()
        await TelegramSDK().send_message(chat_id, 'Мне не удалось отправить этот пост в weibo\n'
                                                  'но можно попробовать еще раз хотя я пробовал это уже 3 раза',
                                         reply_to_message_id=message_id)
        return
    reply_markup = {
        'inline_keyboard': [[
            {"text": "Сообщений успешно отправленно в weibo", "url": settings.WEIBO_HOST_URL},
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
        ]]
    }

    await TelegramSDK().edit_only_message_reply(chat_id, message_id, reply_markup=reply_markup)

    asyncio.ensure_future(send_message_weibo(chat_id, message_id, post_id))


@bot_handler.command(command='statistics')
@users_info
@white_list
async def statistics(message, _request):
    day_to_week = [
        'понедельник',
        'вторник',
        'среда',
        'четверг',
        'пятница',
        'суббота',
        'воскресенье'
    ]

    chat_id = message['user_info']['id']

    create_post_count_list = await DataBase.all("""
select date_trunc('day', created_at) AS "day" , count(*)
from post
WHERE created_at > now() - interval '7 days'
GROUP BY 1
order by 1 DESC;""")

    send_weibo_count_list = await DataBase.all("""
select date_trunc('day', created_at) AS "day" , min(created_at), 
    max(created_at), count(*)
from post
WHERE created_at > now() - interval '7 days' and
      status_posted is TRUE
GROUP BY 1
order by 1 DESC;""")

    create_post_count_text = '\n'.join([f'{i.day.strftime("%d.%m")} - {i.count}' for i in create_post_count_list])
    send_weibo_count_text = '\n'.join([f'{i.day.strftime("%d.%m")} - {i.count}' for i in send_weibo_count_list])

    schedule_work = '\n'.join([f'{i.day.strftime("%d.%m")} [{day_to_week[i.day.weekday()]}] c {i.min.strftime("%H:%M")} до {i.max.strftime("%H:%M")}'
                               for i in send_weibo_count_list])

    message = 'Статистика за неделю в формате (дата, количество)\n\n'
    if send_weibo_count_text:
        message += 'Постов было отправленно в weibo: \n```\n' \
                    f'{send_weibo_count_text} ```\n\n'

    if create_post_count_text:
        message += 'Постов было записано в базу: \n```\n' \
                    f'{create_post_count_text} \n```\n\n'

    if schedule_work:
        message += 'Примерный рафик рабоыт: \n```\n' \
                    f'{schedule_work} ```'

    await TelegramSDK().send_message(
        chat_id=chat_id,
        message=message
    )


@bot_handler.text()
@users_info
@white_list
async def test_message(message, _request):
    chat_id = message['user_info']['id']

    message_text = message['message']['text']
    message_id = message['message']['message_id']

    # todo нужно изучить способ расопзнания текста
    if 'спасиб' in message_text:
        await TelegramSDK().send_message(chat_id=chat_id, message=get_thank_message(), reply_to_message_id=message_id)
