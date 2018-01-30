# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "y^g$^26uo^zogzogzog=amp^dn-zwm!v(q!5=(4^sc_!!!y6n"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_postgresql_light_schemas",
    "testing_app",
]

DATABASES = {
    'default': {
        'ENGINE': 'django_postgresql_light_schemas.engine',
        'NAME': 'test_django_light',
        'OPTIONS': {
                'options': '-c search_path=foo,bar'
        },
        'USER': 'test_django_light_user',
        'PASSWORD': 'test_django_light_passwd',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_test_django_light',
            'CHARSET': 'UTF-8',
            'TEMPLATE': 'template0',
        },
    },
}

SUPPORTED_SCHEMAS = (
    'foo',
    'bar',
)

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
