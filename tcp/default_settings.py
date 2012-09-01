#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Django settings for tcp project.
import os

from django.core.urlresolvers import reverse_lazy

HERE = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Are we running the tests or a real server?
TESTS = False

ADMINS = ()
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Paris'

LANGUAGE_CODE = 'en-us'
LANGUAGES = (
        ('en', 'en-us'),
        ('fr', 'fr-fr'),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(HERE, 'public', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(HERE, 'public', 'static')
STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'ratelimitbackend.backends.RateLimitModelBackend',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
    'ratelimitbackend.middleware.RateLimitMiddleware',
)

ROOT_URLCONF = 'tcp.urls'

TEMPLATE_DIRS = (
    os.path.join(HERE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.messages',

    'floppyforms',
    'password_reset',
    'raven.contrib.django',
    'south',

    'tcp.core',
)

LOCALE_PATHS = (
    os.path.join(HERE, 'locale'),
)

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('core:home')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'ratelimitbackend': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
        },
        'raven': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sentry.errors': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {
        'dsn': 'https://9fc4036179ca4b278a28e608b5d4f236:'
               '3830fa98b1894486b6387a511f1eb9ff@app.getsentry.com/2247',
}
