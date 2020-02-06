from .base import *

import dj_database_url

DATABASES = {"default": dj_database_url.config()}

ALLOWED_HOSTS = ["backend-apis-django.herokuapp.com"]

DEBUG = False

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware",] + MIDDLEWARE

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
