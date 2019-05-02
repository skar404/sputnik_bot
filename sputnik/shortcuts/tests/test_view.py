from sputnik.shortcuts.view import success, bad_request, marshmallow_errors


def test_success():
    response = success()

    assert response.text == '{"status": "SUCCESS"}'
    assert response.status == 200


def test_success_message():
    response = success(message='ping')

    assert response.text == '{"status": "SUCCESS", "result": "ping"}'
    assert response.status == 200


def test_bad_request():
    response = bad_request()

    assert response.text == '{"status": "ERROR", "error": "bad request"}'
    assert response.status == 400


def test_bad_request_message():
    response = bad_request(message='not found', code=404)

    assert response.text == '{"status": "ERROR", "error": "not found"}'
    assert response.status == 404


def test_marshmallow_errors():
    response = marshmallow_errors({'email': 'not found'})

    assert response.text == '{"status": "ERROR", "errors": {"email": "not found"}}'
    assert response.status == 400
