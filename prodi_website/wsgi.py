"""
WSGI config for prodi_website project.
"""
import os
import sys

path = '/home/meilanaafif2405/project_akhir'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'prodi_website.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()