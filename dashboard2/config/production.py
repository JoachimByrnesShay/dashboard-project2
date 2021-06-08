# Settings that are unique to production go here
from .base import *
import os

from dotenv import load_dotenv
import dj_database_url
db_password = os.getenv('DB_PASSWORD')

DEBUG = False

DATABASES = { 'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME':'', 'USER':'', 'PASSWORD':'', 'HOST': '', 'PORT':'',}} 

# Heroku: Update database configuration from $DATABASE_URL.

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())


#STATIC_URL = 'static'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
print(STATICFILES_DIRS)
print(STATIC_ROOT)

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'