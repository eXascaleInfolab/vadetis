# project imports
from .common import *

# turn off all debugging
DEBUG = False

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOSTS = ['localhost', 'vadetis.exascale.info']

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

# ##### SECURITY CONFIGURATION ############################

# TODO: Make sure, that sensitive information uses https
# TODO: Evaluate the following settings, before uncommenting them
# redirects all requests to https
# SECURE_SSL_REDIRECT = True
# session cookies will only be set, if https is used
# SESSION_COOKIE_SECURE = True
# how long is a session cookie valid?
# SESSION_COOKIE_AGE = 1209600
# LANGUAGE_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


# the email address, these error notifications to admins come from
# SERVER_EMAIL = 'root@localhost'

# how many days a password reset should work. I'd say even one day is too long
# PASSWORD_RESET_TIMEOUT_DAYS = 1