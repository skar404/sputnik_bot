import base64
import os

from envparse import env
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_envfile(os.path.join(BASE_DIR, '.env'))


# Setting Gunicorn App
WORKERS: int = env.int('WORKERS', default=1)

TIME_OUT: int = env.int('TIME_OUT', default=300)

BOT_TOKEN: str = env.str('BOT_TOKEN', default=None)
BOT_SECRET_URL: str = env.str('BOT_SECRET_URL', default='bot')
BOT_WEB_HOOK: str = env.str('BOT_WEB_HOOK', default=None)

RSS_FEED: str = env.str('RSS_FEED', default=None)
SHORT_LINK: str = env.str('SHORT_LINK', default=None)

WEIBO_APP_KEY: str = env.str('WEIBO_APP_KEY', default=None)
WEIBO_APP_SECRET: str = env.str('WEIBO_APP_SECRET', default=None)
WEIBO_APP_HOST: str = env.str('WEIBO_APP_HOST', default=None)

WEIBO_LOGIN: str = env.str('WEIBO_LOGIN')
WEIBO_PASSWORD: str = env.str('WEIBO_PASSWORD')

DB_DSN: str = env.str('DB_DSN', default='postgres://postgres:postgres@127.0.0.1:5400/postgres')

POST_USER: List[str] = env.list('POST_USER', default=[])
ADMIN_USER: List[str] = env.list('ADMIN_USER', default=[])

JWT_SECRET = env.str('JWT_SECRET', default='')

ANTI_CAPTCHA_KEY = env.str('ANTI_CAPTCHA_KEY', default='')
