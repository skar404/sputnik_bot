import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_envfile(os.path.join(BASE_DIR, '.env'))


# Setting Gunicorn App
WORKERS = env.int('WORKERS', default=1)

TIME_OUT = env.int('TIME_OUT', default=300)

BOT_TOKEN = env.str('BOT_TOKEN')
BOT_WEB_HOOK = env.str('BOT_WEB_HOOK')
