"""
Django settings for ddnsbroker project.
"""

import os

SECRET_KEY = '!%3a@3lh!0y48x$=-^dkuj6z&__t=hloh7*pkqe=76#^q+4%tr'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ddnsbroker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ddnsbroker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },

    }
]

WSGI_APPLICATION = 'ddnsbroker.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'stderr': {
            'format': '[{asctime}] {message}',
            'style': '{',
        },
        'stderr_level': {
            'format': '[{asctime}] {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'stderr',
        },
        'stderr_level': {
            'class': 'logging.StreamHandler',
            'formatter': 'stderr_level',
        },
    },
    'loggers': {
        'ddnsbroker': {
            'handlers': ['stderr_level'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['stderr'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
