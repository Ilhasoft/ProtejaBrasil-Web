"""
Django settings for protejabrasil project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django.conf.global_settings as DEFAULT_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 18,
    'streetViewControl': True,
    'center': {'lat': -14.2392976, 'lng': -53.1805017}
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move'
}

# Application definition

INSTALLED_APPS = (
    'flat',
    'geoposition',
    'sorl.thumbnail',
    'apps.theme',
    'apps.uf',
    'apps.permission',
    'apps.user',
    'apps.protectionnetwork',
    'apps.violation',
    'apps.authorization',
    'apps.importation',
    'apps.log',
    'apps.feedback',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
)

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'X-CSRFToken'
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'OPTIONS'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'protejabrasil.urls'

WSGI_APPLICATION = 'protejabrasil.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',
        'PORT': '5432',
    }
}

SITE_URL = 'protejabrasil.ilhasoft.mobi'

AUTH_USER_MODEL = 'user.Users'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.AllowAny',
    ),
    # 'PAGINATE_BY': 10,  # Default to 10
    # 'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    # 'MAX_PAGINATE_BY': 100,
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Maceio'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticbuild/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)


TEMPLATE_CONTEXT_PROCESSORS = (
                                  'django.contrib.auth.context_processors.auth',
                                  'django.core.context_processors.debug',
                                  'django.core.context_processors.i18n',
                                  'django.core.context_processors.media',
                                  'django.core.context_processors.static',
                                  "django.core.context_processors.tz",
                                  'django.contrib.messages.context_processors.messages',
                                  'django.core.context_processors.request',
                                  'apps.utils.custom_context_processors.custom_context_processors.user_auth',
                              ) + DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS

DEFAULT_FROM_EMAIL = 'your_from_email'
SERVER_EMAIL = 'your_server_email'
EMAIL_HOST = 'your_email_host'
EMAIL_HOST_USER = 'your_email_host_user'
EMAIL_HOST_PASSWORD = 'your_email_host_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_ALIAS = 'your_email_alias'

SWAGGER_SETTINGS = {
    'api_version': '0.1',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post'
    ],
    'info': {
        'title': 'API Proteja Brasil',
        'description': 'Remember to include in the request header parameter "Authorization" with the token generated in the back-end application'
    }
}

try:
    from .local_settings import *
except ImportError:
    pass
