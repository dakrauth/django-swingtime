import os, sys

ROOT_DIR = '/var/www/swingtime.com/'

sys.path.extend([ROOT_DIR,])
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.chdir(ROOT_DIR)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

