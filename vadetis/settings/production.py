import environ
env = environ.Env()

from .common import *

# turn off all debugging
DEBUG = False

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'vadetis.exascale.info']

# ##### MAIL CONFIGURATION ###############################

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = env('EMAIL_ADDRESS')

# ##### Tokens #############################

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

# MAP BOX - ACCOUNT
MAPBOX_USER = env('MAPBOX_USER')
MAPBOX_ACCOUNT = env('MAPBOX_ACCOUNT')
MAPBOX_PW = env('MAPBOX_PW')
MAPBOX_TOKEN = env('MAPBOX_TOKEN')

# ##### DATABASE CONFIGURATION ############################

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
     'default': env.db()
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS

# ##### SECURITY CONFIGURATION ############################

SECRET_KEY = env('SECRET_KEY')

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


