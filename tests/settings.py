import datetime
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "swingtime-tests"
DEBUG = False
ALLOWED_HOSTS = ["*"]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = ["django.contrib.contenttypes", "swingtime"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "tests", BASE_DIR / "demo/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": ["django.template.context_processors.request"],
        },
    },
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
if django.VERSION < (5, 0):
    FORM_RENDERER = "django.forms.renderers.DjangoDivFormRenderer"


SWINGTIME = {
    "TIMESLOT_START_TIME": datetime.time(14),
    "TIMESLOT_END_TIME_DURATION": datetime.timedelta(hours=6.5),
}
