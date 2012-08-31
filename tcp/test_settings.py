#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('always')

from default_settings import *  # noqa

SECRET_KEY = 'test secret key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

TESTS = True

EMAIL_HOST = 'dummy'
