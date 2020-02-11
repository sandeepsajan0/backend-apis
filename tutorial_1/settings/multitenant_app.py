from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

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

AUTH_USER_MODEL = "multitenant_app.User"
