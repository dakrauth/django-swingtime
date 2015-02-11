try:
    # dateutil is an absolute requirement
    import dateutil
except ImportError:
    raise ImportError('django-swingtime requires the "python-dateutil" package')

DEBUG = TEMPLATE_DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'swingtime_test.db'}}
TIME_ZONE = 'America/New_York'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = 'swingtime_test'
TEMPLATE_CONTEXT_PROCESSORS = ('swingtime.context_processors.current_datetime',)
ROOT_URLCONF = 'urls'
INSTALLED_APPS = ('django.contrib.contenttypes', 'swingtime',)
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',)
SWINGTIME_SETTINGS_MODULE = 'swingtime_settings'
