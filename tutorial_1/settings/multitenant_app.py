from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django_multitenant.backends.postgresql",
        "NAME": os.getenv("DBNAME"),
        "user": os.getenv("DBUSER"),
        "password": os.getenv("DBPASSWORD"),
    }
}

INSTALLED_APPS += [
    "multitenant_app",
]
APPEND_SLASH = True

AUTH_USER_MODEL = "multitenant_app.User"
