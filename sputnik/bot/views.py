import asyncio
import logging
import time

from sputnik import settings
from sputnik.clients.file_download import download_img
from sputnik.clients.telegram.client import TelegramSDK, ChatTelegramSDK
from sputnik.bot.router import TelegramRouter
from sputnik.clients.weibo_parser import WeiboParserService
from sputnik.models.main import DataBase
from sputnik.models.post import PostModel
from sputnik.settings import BOT_TOKEN
from sputnik.shortcuts.main import users_info, white_list, get_thank_message
from sputnik.utils.telegram import get_start_post_reply_markup
from sputnik.utils.text import get_post_text, is_valid_post, is_lightning

bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


@bot_handler.command(command='start')
@users_info
@white_list
async def command_start(message, _request):
    user_name = message['message']['from'].get('username')

    text = f'Привет @{user_name},\n' \
        'Данный бот уже настроен и теперь ты будешь получать уведомления о всех новостях\n' \
        f'Бот обнволяет посты раз в {settings.UPDATE_POST_SECONDS} секунд и\n' \
        f'отправлет их в telegram раз в {settings.SEND_POST_SECONDS} секунд.'
    await TelegramSDK().send_message(chat_id=message['message']['chat']['id'], message=text)


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
        photo_id = None
        if image is not None:
            photo_id = await weibo_service.get_id_and_push_image(image, settings.WEIBO_NICK)
        await weibo_service.create_post(text, photo_id)


async def send_message_weibo(telegram_sdk: ChatTelegramSDK, post_id):
    start_time = time.time()

    post: PostModel = await PostModel.query.where(PostModel.id == post_id).gino.first()

    if is_valid_post(post.enclosure) is False and is_lightning(post) is False:
        logging.exception('not valid post')
        await telegram_sdk.chat_send_message(message="новость не соотвествует условию и не была отпарвленна в weibo")
        return

    if post.status_posted is True:
        logging.exception('error post status_posted is True')
        await telegram_sdk.chat_send_message(message="новость уже была отправленна в weibo")
        return

    await post.update(status_posted=True).apply()

    text = get_post_text(post)
    image = await download_img(post.enclosure)
    is_err = True
    for _ in range(3):
        try:
            await post_to_weibo(text, image)
            is_err = False
            break
        except Exception:
            logging.exception('error send waibo')

    if is_err:
        logging.exception('error send post to weibo')
        await post.update(status_posted=False).apply()
        # обновляем кнопки чтобы можно было повторно отправить пост
        await telegram_sdk.chat_edit_only_message_reply(
            reply_markup=get_start_post_reply_markup(url=post.guid, post_id=post.id)
        )
        await telegram_sdk.chat_send_message(
            message='Мне не удалось отправить этот пост в weibo\n'
                    'но можно попробовать еще раз хотя я пробовал это уже 3 раза',
        )
        return
    reply_markup = {
        'inline_keyboard': [[
            {"text": "Сообщений успешно отправленно в weibo", "url": settings.WEIBO_HOST_URL},
        ]]
    }
    await telegram_sdk.chat_edit_only_message_reply(reply_markup=reply_markup)

    end_time = time.time() - start_time

    text_send_count = ''
    try:
        curs = await DataBase.first("""select count(1) as count from post 
        WHERE created_at >= now()::date and status_posted is TRUE;""")
        send_count = curs.count

        if send_count == 1 or send_count == '1':
            text_send_count = f'Это ваш первый пост в Weibo сегодня\n' \
                              f'По этой причине я хочу пожелать вам удачного рабочего дня и возможно доброго утра :)\n' \
                              f'Всегда ваш - Бот v2019.1\n'
        elif send_count:
            text_send_count = f'Сегодня я уже отправил {send_count}/25 постов\n'
    except Exception:
        logging.exception('error connect db')

    await telegram_sdk.chat_send_message(f'{text_send_count}Я успешно отправил в weibo, время: {end_time}')


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
    telegram = ChatTelegramSDK(chat_id=chat_id, message_id=message_id)

    reply_markup = {
        'inline_keyboard': [[
            {"text": "Сообщений скоро будет отправленно в weibo", "url": settings.WEIBO_HOST_URL},
        ]]
    }

    await telegram.chat_edit_only_message_reply(reply_markup=reply_markup)
    asyncio.ensure_future(send_message_weibo(telegram_sdk=telegram, post_id=post_id))


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

    schedule_work = '\n'.join([f'{i.day.strftime("%d.%m")} [{day_to_week[i.day.weekday()]}] c '
                               f'{i.min.strftime("%H:%M")} до {i.max.strftime("%H:%M")}'
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
