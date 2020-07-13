"""
Django settings for vadetis project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u)0a*o(9z(*wcrj8$wq421r0g&4xd0@e&2)2kzum5p2=9@=_z9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# MAX POST SIZE INCREASED FOR LARGE DATASETS
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# MAX NUMBER OF VALUES FOR A DATASET
DATASET_MAX_VALUES = 100000
# scikit's TRAIN TEST SPLIT DOES REQUIRE AT LEAST NORMAL 20 VALUES AND 5 ANOMALIES TO MAKE A MINIMAL SPLIT INTO TRAIN, VALID AND TEST SET
# AS THE SET CAN BE SPLIT IN A RANGE FROM 20% TO 80%
TRAINING_DATASET_MIN_NORMAL = 20
TRAINING_DATASET_MIN_ANOMALIES = 5
TRAINING_DATA_MAX_SIZE = 10000
TRAINING_DATA_MIN_SIZE = 500

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # required for django-allauth
    'django_extensions',  # needed for jupyter notebooks
    'vadetisweb',
    'django_celery_results',
    'django_bootstrap_breadcrumbs',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'rest_framework_datatables',
    'drf_yasg',
    'captcha'
]

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

ROOT_URLCONF = 'vadetis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # global templates, e.g. admin backend
            os.path.join(BASE_DIR, 'vadetisweb', 'templates'),  # vadetisweb site templates
            os.path.join(BASE_DIR, 'vadetisweb', 'templates', 'allauth')  # vadetisweb allauth templates
        ],
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

WSGI_APPLICATION = 'vadetis.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of django-allauth
    'django.contrib.auth.backends.ModelBackend',

    # django-allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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
    # or allow read-only access for unauthenticated users.

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

SOCIALACCOUNT_FORMS = {
    'login': 'allauth.socialaccount.forms.DisconnectForm',
    'signup': 'vadetisweb.forms.SocialAccountSignupForm',
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client credentials, or list them here:
        # ATTENTION: there might be a bug in allauth, add this info in admin backend under socialapplications
        'APP': {
            'client_id': '844915385364-2aeu7mjtg4s9v1beb1gp8lmqjpr2lpi5.apps.googleusercontent.com',
            'secret': 'SQ7jfMEvIBGNHiDfVpyI6OMr',
            'key': 'AIzaSyCWVgicKlJ9mnTyjSnY9Mb-yGO96RnMDeA'
        }
    }
}

SITE_ID = 1

# Cookies
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# CHANGE ON PRODUCTION (!!)
"""
Whether to use a secure cookie for the session cookie. If this is set to True, the cookie will be marked as “secure”, which means browsers may ensure that the cookie is only sent under an HTTPS connection.
Leaving this setting off isn’t a good idea because an attacker could capture an unencrypted session cookie with a packet sniffer and use the cookie to hijack the user’s session.
"""
SESSION_COOKIE_SECURE = False

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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# Django Registration Redux
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
REGISTRATION_OPEN = True  # set to False to disable User registration
REGISTRATION_SALT = 'encoded_username:timestamp:signature'

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# CELERY CONFIG
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_TASK_RESULT_EXPIRES = timedelta(days=30)
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TIMEZONE = 'Europe/Zurich'

# BREADCRUMBS
BREADCRUMBS_TEMPLATE = 'vadetisweb/parts/breadcrumbs.html'
