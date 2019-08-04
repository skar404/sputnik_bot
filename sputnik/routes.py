from sputnik.bot.views import bot_handler
from sputnik.settings import BOT_SECRET_URL
from sputnik.views import ping, bot


def setup_routes(app):
    bot_handler.register()

    app.router.add_post('/bot{}'.format(BOT_SECRET_URL), bot, name='bot')
    app.router.add_get('/ping', ping, name='ping')
