import os
from dotenv import load_dotenv

load_dotenv()

DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or 'will-be-changed-in-production'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
DJANGO_ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',') if host.strip()]
DATABASE_URL = os.environ.get('DATABASE_URL')
PG_DB = os.environ.get('PG_DB')
PG_USER = os.environ.get('PG_USER')
PG_PASSWORD = os.environ.get('PG_PASSWORD')
PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
REDIS_URL = os.environ.get('REDIS_URL') or os.environ.get('REDIS_HOST')
ALLOW_ANONYMOUS_VOTE = os.environ.get('ALLOW_ANONYMOUS_VOTE', '0') == '1'
