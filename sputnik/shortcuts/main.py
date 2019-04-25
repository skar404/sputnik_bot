from sputnik import settings
from sputnik.models.user import UserModel


def users_info(func):
    async def wrapper(request, *args, **kwargs):
        user_info = {}

        if 'message' in request:
            user_info = request['message']
        elif 'callback_query' in request:
            user_info = request['callback_query']
        user_info = user_info.get('from')

        if user_info is None:
            return

        request['user_info'] = user_info
        user_id = user_info['id']

        user = await UserModel.query.where(UserModel.telegram_id == user_id).gino.first()
        if user is None:
            await UserModel.create(
                telegram_id=user_id,
                info_json={'user_info': user_info}
            )

        res = await func(request, *args, **kwargs)
        return res

    return wrapper


def white_list(func):
    async def wrapper(request, *args, **kwargs):
        user_from_id = request['user_info']['id']

        res = None
        if str(user_from_id) in settings.WHITE_LIST_USER:
            await func(request, *args, **kwargs)
        return res

    return wrapper
