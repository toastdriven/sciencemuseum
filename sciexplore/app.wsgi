import site
site.addsitedir('/srv/django-apps/cosmos.natimon.com/sciencemuseum/sciexplore/ve/lib/python2.6/site-packages')

import os, sys

sys.stdout = sys.stderr # Avoid 'sys.stdout access restricted by mod_wsgi'

sys.path.append('/srv/django-apps/cosmos.natimon.com/sciencemuseum')
sys.path.append('/srv/django-apps/cosmos.natimon.com/sciencemuseum/sciexplore')

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE'] = 'sciexplore.settings'
application = WSGIHandler()

