"""
WSGI config for vibetribe project. changed to vibetribe 9/11

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibetribe.settings')
# changed honeyrae to vibetribe 9/11
application = get_wsgi_application()
