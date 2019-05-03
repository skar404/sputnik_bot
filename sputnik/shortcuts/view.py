from aiohttp.web_response import json_response, Response


class ReturnStatus:
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


def success(message: str = None) -> Response:
    res = {}
    if message is not None:
        res.update({'result': message})

    return json_response({
        'status': ReturnStatus.SUCCESS,
        **res
    })


def bad_request(message='bad request', code=400) -> Response:
    return json_response({
        'status': ReturnStatus.ERROR,
        'error': message
    }, status=code)


def marshmallow_errors(errors: dict, code=400) -> Response:
    return json_response({
        'status': ReturnStatus.ERROR,
        'errors': errors
    }, status=code)
