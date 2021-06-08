# Settings that are unique to production go here
from .base import *  # noqa

DEBUG = False


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sitedb',
        'USER': 'mysiteuser',
        'PASSWORD': db_password,
        'HOST': 'localhost',
        'PORT': ''
    }
}

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())

