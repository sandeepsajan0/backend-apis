from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

INSTALLED_APPS += [
    "multitenant_app",
]

AUTH_USER_MODEL = "multitenant_app.User"
