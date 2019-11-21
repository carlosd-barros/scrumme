"""
Django settings for scrumme project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku

from unipath import Path
from decouple import config
from dj_database_url import parse as db_url


#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'tempus_dominus',

    'core',
    'accounts',
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

ROOT_URLCONF = 'scrumme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.child('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scrumme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# https://github.com/jacobian/dj-database-url

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///db.sqlite3',
        cast=db_url,
    )
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Araguaina'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = BASE_DIR.child('staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.child("static"),
]

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR.child('media')

LOGOUT_URL = "/auth/logout/"

# Auth
LOGIN_REDIRECT_URL = 'core:home'

LOGOUT_REDIRECT_URL = 'accounts:login'

# https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_TEMPLATE_PACK = "bootstrap4"

# E-mail
# https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = config("EMAIL_HOST", default="localhost")

EMAIL_PORT = config("EMAIL_PORT", default=25, cast=int)

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)

# https://tempusdominus.github.io/bootstrap-4/Installing/
TEMPUS_DOMINUS_LOCALIZE = True
TEMPUS_DOMINUS_INCLUDE_ASSETS = True

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-age
# SESSION_COOKIE_AGE = 3600000

# https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/
ALLOWED_UPLOAD_FILETYPES = [
    'jpeg','png', 'jpg'
]
ALLOWED_UPLOAD_MAXSIZE = 716800

# Configure Django App for Heroku.
# https://github.com/heroku/django-heroku
django_heroku.settings(locals())


# Config logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

INTERNAL_IPS = ('127.0.0.1',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s:'
                      '%(filename)s:%(lineno)d %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': config('LOG_LEVEL', default='DEBUG'),
            'propagate': False,
        },
        'requests': {
            'handlers': ['null', ],
            'propagate': False,
        },
        'requests_oauthlib': {
            'handlers': ['null', ],
            'propagate': False,
        },
        'urllib3': {
            'handlers': ['null', ],
            'propagate': False,
        }
    }
}
