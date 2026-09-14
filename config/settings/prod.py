import os

from .base import *  # noqa: F401,F403

DEBUG = False

# Fail fast rather than silently falling back to base.py's dev secret key.
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

CORS_ALLOWED_ORIGINS = [o for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if o]
