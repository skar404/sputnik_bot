from sputnik.shortcuts.main import get_thank_message


def test_get_thank_message():
    text = get_thank_message()

    assert type(text) is str
