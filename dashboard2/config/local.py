
from .base import *
from dotenv import load_dotenv
load_dotenv()

db_password = os.getenv('DB_PASSWORD')

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'config.db.sqlite3'),
    }
}

DATABASES = {
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

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

