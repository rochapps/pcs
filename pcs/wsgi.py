"""
WSGI config for pcs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

from pcs import load_env

# Allow Django to find the `app` module by appending the parent directory to
# the PATH variable
base = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base)

load_env.load_env()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pcs.settings")

application = get_wsgi_application()
