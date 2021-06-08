# Settings that are unique to local dev go here
from .base import *
#import os 
from dotenv import load_dotenv
load_dotenv()
db_password = os.getenv('DB_PASSWORD')

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'config.db.sqlite3'),
    }
}


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


INSTALLED_APPS += ['debug_toolbar']

# Add in Debug Toolbar Middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

# Required configuration for debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

