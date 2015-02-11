import os, sys

ROOT_DIR = '/var/www/demo/'
SITE_DIR = ROOT_DIR + 'demo_site'

sys.path.extend([ROOT_DIR, SITE_DIR])
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.chdir(SITE_DIR)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()