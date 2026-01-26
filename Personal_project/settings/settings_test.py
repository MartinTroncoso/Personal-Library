# flake8: noqa

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

APP_VERSION = os.getenv("APP_VERSION", "dev")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
