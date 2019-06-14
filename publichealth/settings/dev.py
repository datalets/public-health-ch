from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGEME!!!'

# SECURITY WARNING: CAREFUL! your dev site is open to the world
ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

BASE_URL = 'http://localhost:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'publichealth-dev.sqlite3',
    }
}

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
] + INSTALLED_APPS + [
    'wagtail.contrib.styleguide',
]

try:
    from .local import *
except ImportError:
    pass
