from ddnsbroker.settings import *
import os

SECRET_KEY = os.environ.setdefault('SECRET_KEY', 'TOTALLY_SECRET_KEY_THAT_I_WILL_NOT_PUT_IN_VCS')

DEBUG = os.environ.setdefault('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'static'

# for postgresql, mysql and others see https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'var/db.sqlite3',
    }
}

# see https://docs.djangoproject.com/en/3.0/topics/logging/#configuring-logging
# LOGGING =

TIME_ZONE = 'Europe/Berlin'
