#!/usr/bin/env bash
set -euo pipefail

python python manage.py makemigrations && python manage.py migrate --noinput
exec gunicorn polls_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --log-level=info