from json import JSONDecodeError

from aiohttp.web_request import Request
from marshmallow import ValidationError

from sputnik.shortcuts.view import marshmallow_errors, bad_request


def validation_shame(schema):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            try:
                data = await request.json()
            except JSONDecodeError:
                return bad_request('error decode json')

            try:
                req = schema().load(data)
            except ValidationError as err:
                return marshmallow_errors(err.messages)

            request['valid_data'] = dict(req)

            res = await func(request, *args, **kwargs)
            return res

        return wrapper

    return decorator
