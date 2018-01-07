import os
import sys
import datetime
import django

try:
    # dateutil is an absolute requirement
    import dateutil
except ImportError:
    raise ImportError('django-swingtime requires the "python-dateutil" package')

dirname = os.path.dirname
sys.path.extend([
    os.path.dirname(__file__),
    os.path.abspath('..'), # relative location of swingtime app
])

DEBUG = True
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'karate.db',
}}
LANGUAGES = (('en', 'English'),)
STATIC_URL = '/static/'
STATIC_ROOT = 'static'
TIME_ZONE = 'America/New_York'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = 'swingtime-demo'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': (os.path.join(dirname(__file__), 'templates'),),
    'OPTIONS': {
        'debug': True,
        'loaders': (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        'context_processors': (
            'django.template.context_processors.debug',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'swingtime.context_processors.current_datetime',
        )
    }
}]
ALLOWED_HOSTS = ['*'] 

ROOT_URLCONF = 'urls'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'swingtime',
    'karate',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SWINGTIME = {
    'TIMESLOT_START_TIME': datetime.time(14),
    'TIMESLOT_END_TIME_DURATION': datetime.timedelta(hours=6.5)
}

try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_extensions',)

