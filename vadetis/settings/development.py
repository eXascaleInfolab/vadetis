# Python imports
from os.path import join
from pathlib import Path

import environ
env = environ.Env()
env.read_env()

# project imports
from .common import *

# uncomment the following line to include i18n
# from .i18n import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

# MAP BOX - ACCOUNT
MAPBOX_USER = env('MAPBOX_USER')
MAPBOX_ACCOUNT = env('MAPBOX_ACCOUNT')
MAPBOX_PW = env('MAPBOX_PW')
MAPBOX_TOKEN = env('MAPBOX_TOKEN')

# ##### MAIL CONFIGURATION ###############################

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = env('EMAIL_ADDRESS')

# ##### DATABASE CONFIGURATION ############################

BASE_DIR = Path(__file__).resolve().parent.parent

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
     'default': env.db()
}


# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS

SECRET_KEY = env('SECRET_KEY')
