import os

from envparse import env
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_envfile(os.path.join(BASE_DIR, '.env'))


# Setting Gunicorn App
ENVIRONMENT: str = env.str('ENVIRONMENT', default='dev')

WORKERS: int = env.int('WORKERS', default=1)

TIME_OUT: int = env.int('TIME_OUT', default=300)

BOT_TOKEN: str = env.str('BOT_TOKEN', default=None)
BOT_SECRET_URL: str = env.str('BOT_SECRET_URL', default='')
BOT_WEB_HOOK: str = env.str('BOT_WEB_HOOK', default='') + BOT_SECRET_URL
BOT_SECRET_CALLBACK: str = env.str('BOT_SECRET_CALLBACK', default='dev')

RSS_FEED: str = env.str('RSS_FEED', default=None)
SHORT_LINK: str = env.str('SHORT_LINK', default=None)

WEIBO_APP_KEY: str = env.str('WEIBO_APP_KEY', default=None)
WEIBO_APP_SECRET: str = env.str('WEIBO_APP_SECRET', default=None)
WEIBO_APP_HOST: str = env.str('WEIBO_APP_HOST', default=None)

WEIBO_LOGIN: str = env.str('WEIBO_LOGIN', default=None)
WEIBO_PASSWORD: str = env.str('WEIBO_PASSWORD', default=None)

WEIBO_TEST_LOGIN: str = env.str('WEIBO_LOGIN', default=None)
WEIBO_TEST_PASSWORD: str = env.str('WEIBO_PASSWORD', default=None)

DB_DSN: str = env.str('DB_DSN', default='postgres://postgres:postgres@127.0.0.1:5400/postgres')
DB_SSL: bool = env.str('DB_SSL', default=True)
# drone ci: postgres://postgres@database:5432/postgres

POST_USER: List[str] = env.list('POST_USER', default=[])
ADMIN_USER: List[str] = env.list('ADMIN_USER', default=[])
WHITE_LIST_USER: List[str] = env.list('WHITE_LIST_USER', default=[])

JWT_SECRET = env.str('JWT_SECRET', default='')

ANTI_CAPTCHA_KEY = env.str('ANTI_CAPTCHA_KEY', default='')

UPDATE_POST_SECONDS = env.int('UPDATE_POST_SECONDS', default=10)
SEND_POST_SECONDS = env.int('SEND_POST_SECONDS', default=10)

WEIBO_HOST_URL = env.str('WEIBO_HOST_URL', default=None)
WEIBO_NICK = env.str('WEIBO_NICK', default=None)

TG_PROXY_URL = env.str('TG_PROXY_URL', default=None)

SENTRY_DSN: str = env.str('SENTRY_DSN', default=None)

DRONE_COMMIT: str = env.str('DRONE_COMMIT', default=None)
