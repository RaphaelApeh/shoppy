from .base import * # NOQA

DEBUG = True

ALLOWED_HOSTS = []

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
