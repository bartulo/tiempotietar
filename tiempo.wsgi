import os, sys
sys.path.append('/home/servidor/django')
sys.path.append('/home/servidor/django/tiempo')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tiempo.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
