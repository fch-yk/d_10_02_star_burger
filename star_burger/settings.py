import os

from environs import Env
from git import Repo

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])

INSTALLED_APPS = [
    'foodcartapp.apps.FoodcartappConfig',
    'restaurateur.apps.RestaurateurConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'phonenumber_field',
    'rest_framework',
    'geo',
]

ROLLBAR_ON = env.bool('ROLLBAR_ON', False)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

if ROLLBAR_ON:
    MIDDLEWARE.append(
        'rollbar.contrib.django.middleware'
        '.RollbarNotifierMiddlewareExcluding404'
    )

ROOT_URLCONF = 'star_burger.urls'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'star_burger.wsgi.application'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DATABASES = {
    'default': env.dj_db_url("DATABASE_URL")
}

pwd_validation_path = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{pwd_validation_path}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{pwd_validation_path}.MinimumLengthValidator',
    },
    {
        'NAME': f'{pwd_validation_path}.CommonPasswordValidator',
    },
    {
        'NAME': f'{pwd_validation_path}.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = env.str('LANGUAGE_CODE', 'ru-RU')

TIME_ZONE = env.str('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

INTERNAL_IPS = [
    '127.0.0.1'
]


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
    os.path.join(BASE_DIR, "bundles"),
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}

YA_API_KEY = env.str('YA_API_KEY')

if ROLLBAR_ON:
    ROLLBAR = {
        'access_token': env('ROLLBAR_POST_SERVER_ITEM_ACCESS_TOKEN'),
        'environment': env('ROLLBAR_ENVIRONMENT', 'development'),
        'code_version': '1.0',
        'branch': Repo(path=BASE_DIR).active_branch.name,
        'root': BASE_DIR,
    }
