import os
import sys
try:
    # dateutil is an absolute requirement
    import dateutil
except ImportError:
    raise ImportError(
        'django-swingtime requires the "dateutil" package '
        '(http://labix.org/python-dateutil): $ pip install python-dateutil'
    )

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SITE_DIR)
sys.path.extend([
    os.path.abspath('..'),    # relative path to karate app
    os.path.abspath('../..'), # relative location of swingtime app
])

DEBUG = TEMPLATE_DEBUG = True
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'karate.db',
}}

TIME_ZONE = 'America/New_York'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(SITE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_DIR, 'static')
STATIC_URL = '/static/'

SECRET_KEY = 'j#_e3y&h=a4)hrmj=)bqo@$6qoz6(hrf9wz@uqq@uy*0uzl#ew'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.contrib.auth.context_processors.auth',
    'swingtime.context_processors.current_datetime',
)

ROOT_URLCONF = 'demo_site.urls'
TEMPLATE_DIRS = (
    os.path.join(SITE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'swingtime',
    'karate',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SWINGTIME_SETTINGS_MODULE = 'demo_site.swingtime_settings'

try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_extensions',)

