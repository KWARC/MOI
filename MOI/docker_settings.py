"""
Django Docker settings for MOI project.
Reads all relevant settings from the environment
"""

from .settings import *
import sys

# No Debugging
DEBUG = False

# we want to allow all hosts
ALLOWED_HOSTS = tuple(os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "").split(","))

# all our sessions be safe
SECRET_KEY = os.environ.setdefault("DJANGO_SECRET_KEY", "")

# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.setdefault("DJANGO_DB_ENGINE", ""),
        'NAME': os.environ.setdefault("DJANGO_DB_NAME", ""),
        'USER': os.environ.setdefault("DJANGO_DB_USER", ""),
        'PASSWORD': os.environ.setdefault("DJANGO_DB_PASSWORD", ""),
        'HOST': os.environ.setdefault("DJANGO_DB_HOST", ""),
        'PORT': os.environ.setdefault("DJANGO_DB_PORT", ""),
    }
}

# Static & Media URLs
STATIC_ROOT = "/var/www/static"
