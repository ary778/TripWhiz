# In tripwhiz/settings.py

import os
import environ
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Initialize django-environ ---
env = environ.Env(
    DEBUG=(bool, False)
)

# --- Read the .env file ---
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# --- Get All Secrets and Settings from .env ---
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

# --- CHANGE: Read two separate API keys instead of one ---
SERPAPI_FLIGHTS_API_KEY = env('SERPAPI_FLIGHTS_API_KEY')
SERPAPI_HOTELS_API_KEY = env('SERPAPI_HOTELS_API_KEY')
# --- END CHANGE ---

try:
    PEXELS_API_KEY = env('PEXELS_API_KEY')
except ImproperlyConfigured:
    PEXELS_API_KEY = ''


# --- Application definition ---
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'travel',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tripwhiz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'tripwhiz.wsgi.application'

# --- Database ---
DATABASES = {
    'default': env.db(),
}

# --- Password validation, Internationalization, Static files ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'