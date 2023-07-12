from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

WSGI_APPLICATION = "config.wsgi.deploy.application"
