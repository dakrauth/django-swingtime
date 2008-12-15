import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = TEMPLATE_DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'karate.db'
TIME_ZONE = 'America/New_York'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'j#_e3y&h=a4)hrmj=)bqo@$6qoz6(hrf9wz@uqq@uy*0uzl#ew'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'swingtime.context_processors.current_datetime',
)

ROOT_URLCONF = 'demo.urls'
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    
    'swingtime',
    'karate',
)

try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)
    
try:
    import dateutil
except ImportError:
    sys.stderr.write('\n*** django-swingtime requires the "dateutil" package\n\n')
    raise
    

SWINGTIME_SETTINGS_MODULE = 'demo.swingtime_settings'