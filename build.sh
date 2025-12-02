#!/usr/bin/env bash
set -euo pipefail

# Install dependencies and collect static files during image build
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput

