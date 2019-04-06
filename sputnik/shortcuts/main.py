def users_info(func):
    async def wrapper(request, *args, **kwargs):
        user_info = None

        if 'message' in request:
            user_info = request['message']['from']

        if user_info:
            pass

        res = await func(request, *args, **kwargs)
        return res

    return wrapper
