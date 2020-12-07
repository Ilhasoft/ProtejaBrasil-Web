"""
Django settings for protejabrasil project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ
import django.conf.global_settings as DEFAULT_SETTINGS


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

environ.Env.read_env(env_file=(environ.Path(__file__) - 2)(".env"))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(lambda v: [s.strip() for s in v.split(",")], "*"),
    LANGUAGE_CODE=(str, "pt-br"),
    TIME_ZONE=(str, "America/Maceio"),
    EMAIL_HOST=((lambda v: v or None), None),
    DEFAULT_FROM_EMAIL=(str, "webmaster@localhost"),
    SERVER_EMAIL=(str, "root@localhost"),
    EMAIL_PORT=(int, 25),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_SSL=(bool, False),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_ALIAS=(str, ""),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

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
DATABASES = {"default": env.db(var="DEFAULT_DATABASE", default="sqlite:///db.sqlite3")}

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

LANGUAGE_CODE = env.str("LANGUAGE_CODE")

TIME_ZONE = env.str("TIME_ZONE")

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

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env.str("SERVER_EMAIL")
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_ALIAS = env.str("EMAIL_ALIAS")

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
