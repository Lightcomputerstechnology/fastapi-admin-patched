import threading

_locale = threading.local()


def get_locale() -> str:
    return getattr(_locale, "value", "en_US")


def set_locale(value: str):
    _locale.value = value
