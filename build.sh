#!/usr/bin/env bash
set -euo pipefail

# Install dependencies and collect static files during image build
python -m pip install -r requirements.lock
python manage.py collectstatic --noinput

