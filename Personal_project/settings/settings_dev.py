# flake8: noqa

from .base import *

DEBUG = True
ALLOWED_HOSTS: list[str] = []

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
]

CSRF_COOKIE_SECURE = False  # in local
SESSION_COOKIE_SECURE = False  # in local

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
