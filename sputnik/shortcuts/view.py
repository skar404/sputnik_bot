from aiohttp.web_response import json_response


class ReturnStatus:
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


def success(message: str = None):
    res = {}
    if message is not None:
        res.update({'result': message})

    return json_response({
        'status': ReturnStatus.SUCCESS,
        **res
    })


def bad_request(message='bad request'):
    return json_response({
        'status': ReturnStatus.ERROR,
        'error': message
    }, status=400)


def marshmallow_errors(errors: dict):
    return json_response({
        'status': ReturnStatus.ERROR,
        'errors': errors
    }, status=400)
