import os, sys
sys.stdout = sys.stderr
sys.path.extend(['/var/www/swingtime'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

