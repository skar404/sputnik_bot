from sputnik.bot.views import bot_handler
from sputnik.views import ping, bot, waibo


def setup_routes(app):
    bot_handler.register()

    app.router.add_post('/bot', bot, name='bot')
    app.router.add_get('/waibo', waibo, name='waibo')
    app.router.add_get('/', ping, name='ping')
