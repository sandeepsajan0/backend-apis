import dj_database_url

DATABASES = {"default": dj_database_url.config()}

ALLOWED_HOSTS = ["backend-apis-django.herokuapp.com"]

DEBUG = False

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "tutorial_app.middleware.CustomAuthMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
