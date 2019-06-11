from sputnik.settings import BOT_SECRET_CALLBACK


def get_secret_callback(callback_name: str) -> str:
    return f'secret:{BOT_SECRET_CALLBACK}:{callback_name}'


def get_start_post_reply_markup(url, post_id):
    return {
        'inline_keyboard': [[
            {"text": f"к новости", "url": url},
        ], [
            {"text": "Запостить", "callback_data": f'post_message:id:{post_id}'},
        ]]
    }
