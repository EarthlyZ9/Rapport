#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.deploy

cd /home/rapport
python3 manage.py migrate || exit 1

exec celery -A config worker --loglevel=info \
"$@"