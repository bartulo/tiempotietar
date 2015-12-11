"""
Django settings for tiempo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'situ%w*6su$7x#-b*uqnwz3)%6ac(icj6o4@6g14q&ezgd69ej'

# SECURITY WARNING: don't run with debug turned on in production!

if socket.gethostname() == 'netbook':
  DEBUG = True
  TEMPLATE_DEBUG = True

else:
  DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'south',
    'smart_selects',
    'bootstrap3',
    'django_twilio',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tiempo.urls'

WSGI_APPLICATION = 'tiempo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if socket.gethostname() == 'netbook':
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tiempo2',
        'USER': 'nano',
        'PASSWORD': 'ventanuco',
        'HOST': '', 
    }
}
else:
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tiempo',
        'USER': 'servidor',
        'PASSWORD': 'ventanuco',
        'HOST': 'localhost', 
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'tiempodata')
MEDIA_URL = '/media/'

# Redirect when login is correct.
LOGIN_REDIRECT_URL = "/"
# Redirect when login is not correct.
LOGIN_URL = '/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tiempoaltiempotietar@gmail.com'
EMAIL_HOST_PASSWORD = 'admintietar'
EMAIL_PORT = 587
TWILIO_ACCOUNT_SID = 'AC07c70918885cfa85e469b95f4f81a522'
TWILIO_AUTH_TOKEN = '2fa4f6c349d5e12a1439eff61a570abb'
