import os

from envparse import env

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
