import os
import sys
import django
try:
    # dateutil is an absolute requirement
    import dateutil
except ImportError:
    raise ImportError('django-swingtime requires the "python-dateutil" package')

dirname = os.path.dirname
sys.path.extend([
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

_DJ_GT_17 = django.VERSION >= (1,8)
__TEMPLATE_DEBUG = False
__TEMPLATE_DIRS = (os.path.join(dirname(__file__), 'templates'),)
__TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
__TEMPLATE_CONTEXT_PROCESSORS = (
    'django.{}.context_processors.debug'.format('template' if _DJ_GT_17 else 'core'),
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'swingtime.context_processors.current_datetime',
)

if _DJ_GT_17:
    TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': __TEMPLATE_DIRS,
        'OPTIONS': {
            'debug': True,
            'loaders': __TEMPLATE_LOADERS,
            'context_processors': __TEMPLATE_CONTEXT_PROCESSORS
        }
    }]
else:
    TEMPLATE_DEBUG = __TEMPLATE_DEBUG
    TEMPLATE_DIRS = __TEMPLATE_DIRS
    TEMPLATE_LOADERS = __TEMPLATE_LOADERS
    TEMPLATE_CONTEXT_PROCESSORS = __TEMPLATE_CONTEXT_PROCESSORS
    

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SWINGTIME_SETTINGS_MODULE = 'swingtime_settings'

try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_extensions',)

