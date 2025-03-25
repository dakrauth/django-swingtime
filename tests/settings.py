import datetime
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "swingtime-tests"
DEBUG = False
ALLOWED_HOSTS = ["*"]
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "swingtime.urls"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "swingtime",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "tests", BASE_DIR / "tests/old_templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": ["django.template.context_processors.request"],
        },
    },
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
if django.VERSION < (5, 0):
    FORM_RENDERER = "django.forms.renderers.DjangoDivFormRenderer"


SWINGTIME = {
    "TIMESLOT_START_TIME": datetime.time(14),
    "TIMESLOT_END_TIME_DURATION": datetime.timedelta(hours=6.5),
    "URL_VERSION_3": False,
}
