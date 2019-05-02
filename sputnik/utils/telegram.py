from sputnik.settings import BOT_SECRET_CALLBACK


def get_secret_callback(callback_name: str) -> str:
    return f'secret:{BOT_SECRET_CALLBACK}:{callback_name}'
