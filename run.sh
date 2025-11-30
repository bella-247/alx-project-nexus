#!/usr/bin/env bash

python manage.py migrate --noinput

gunicorn polls_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --log-level=info