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

# DJOSER = {
#     # 'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
#     # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
#     # 'ACTIVATION_URL': '#/activate/{uid}/{token}',
#     # 'SEND_ACTIVATION_EMAIL': True,
#     # 'SERIALIZERS': {},
# }

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# Logging
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {"console": {"class": "logging.StreamHandler",},},
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
#         },
#     },
# }

AUTH_USER_MODEL = "multitenant_app.User"
