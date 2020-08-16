# Python imports
import os
from os.path import abspath, basename, dirname, join, normpath
import sys

# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
    join(PROJECT_ROOT, 'vadetisweb', 'templates'),  # vadetisweb site templates
    join(PROJECT_ROOT, 'vadetisweb', 'templates', 'allauth')  # vadetisweb allauth templates
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

# ##### APPLICATION CONFIGURATION #########################

# MAX HTTP POST SIZE
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # = 20 MiB

# MAX NUMBER OF VALUES FOR A DATASET
DATASET_MAX_VALUES = 100000
# scikit's TRAIN TEST SPLIT DOES REQUIRE AT LEAST NORMAL 20 VALUES AND 5 ANOMALIES TO MAKE A MINIMAL SPLIT INTO TRAIN, VALID AND TEST SET
# AS THE SET CAN BE SPLIT IN A RANGE FROM 20% TO 80%
TRAINING_DATASET_MIN_NORMAL = 20
TRAINING_DATASET_MIN_ANOMALIES = 5
TRAINING_DATA_MAX_SIZE = 100000
TRAINING_DATA_MIN_SIZE = 100

# these are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # required for django-allauth
    'django_extensions',  # needed for jupyter notebooks
    'vadetisweb',
    'django_bootstrap_breadcrumbs',
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework_datatables',
    'drf_yasg',
    'captcha'
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'vadetisweb.middleware.cookie_middleware.UserCookieMiddleWare',
]

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # required for django-allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = False
USE_L10N = True
USE_TZ = True


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of django-allauth
    'django.contrib.auth.backends.ModelBackend',

    # django-allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # Use Django's standard 'django.contrib.auth' permissions,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
          'rest_framework.parsers.FormParser',
          'rest_framework.parsers.MultiPartParser',
          'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SWAGGER_SETTINGS = {
    'JSON_EDITOR': True,
}

# Login - Config
LOGIN_REDIRECT_URL = 'vadetisweb:index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'vadetisweb:index'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_VALIDATORS = 'vadetisweb.validators.username_validators'

ACCOUNT_FORMS = {
    'login': 'vadetisweb.forms.AccountLoginForm',
    'signup': 'vadetisweb.forms.AccountSignUpForm',
    'reset_password': 'vadetisweb.forms.AccountResetPasswordForm',
    'reset_password_from_key': 'vadetisweb.forms.AccountResetPasswordKeyForm',
    'disconnect': 'vadetisweb.forms.AccountSocialDisconnectForm',
}

SITE_ID = 1

# Cookies
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6Lc452UUAAAAAFYADmbUZgYf7qBx3A8i-nnLUde2'
RECAPTCHA_PRIVATE_KEY = '6Lc452UUAAAAAA-XsnkMfh7xA-HhzN8Oliq4dZED'

# MAILING - CHANGE MAIL SETTINGS WHEN GOING PRODUCTION!
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lisaexascale@gmail.com'
EMAIL_HOST_PASSWORD = 'svQcdxXQ'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# MAP BOX - ACCOUNT
MAPBOX_USER = 'vadetis'
MAPBOX_ACCOUNT = 'lisaexascale@gmail.com'
MAPBOX_PW = 'J*V6%gsIxWjp'
MAPBOX_TOKEN = 'pk.eyJ1IjoidmFkZXRpcyIsImEiOiJja2NiMTB4NW8yMHI2MnRvMHk2aDl6ZG5kIn0.5CarskUSNdP8fWdvSx7Omw'

# Django Registration Redux
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
REGISTRATION_OPEN = True  # set to False to disable User registration
REGISTRATION_SALT = 'encoded_username:timestamp:signature'

# BREADCRUMBS
BREADCRUMBS_TEMPLATE = 'vadetisweb/parts/breadcrumbs.html'

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

# these persons receive error notification
ADMINS = (
    ('your name', 'your_name@example.com'),
)
MANAGERS = ADMINS

# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# ##### DEBUG CONFIGURATION ###############################
DEBUG = False

# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)

