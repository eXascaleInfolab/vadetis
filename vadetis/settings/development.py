# Python imports
from os.path import join

# project imports
from .common import *

# uncomment the following line to include i18n
# from .i18n import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# ##### MAIL CONFIGURATION ###############################
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lisaexascale@gmail.com'
EMAIL_HOST_PASSWORD = 'svQcdxXQ'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ##### DATABASE CONFIGURATION ############################

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vadetisv2',
        'USER': 'vadetisadmin',
        'PASSWORD': 'Cast40analysts5Roofing',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS