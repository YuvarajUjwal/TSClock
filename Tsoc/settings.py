from pathlib import Path
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'x*x*x*x*********'

DEBUG = True

ALLOWED_HOSTS = ['*','tangosixoclock.in']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tango',
    'captcha',
    'storages',
    'boto3',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'Tsoc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'tango/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SITE_ID = 3

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT = '/'

SOCIALACCOUNT_PROVIDERS = { 
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online','prompt': 'select_account',},
    }
}
SOCIALACCOUNT_LOGIN_ON_GET = True

WSGI_APPLICATION = 'Tsoc.wsgi.application'

CSRF_TRUSTED_ORIGINS = [
    'https://www.tangosixoclock.in',
]

CSRF_ALLOWED_ORIGINS = ["https://www.tangosixoclock.in"]
CORS_ORIGINS_WHITELIST = ["https://www.tangosixoclock.in"]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

MEDIA_URL = '/images/'

MEDIA_ROOT = os.path.join(BASE_DIR,"static/images/")



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_USE_TLS = True 

EMAIL_HOST_USER = 'xxxx@gmail.com'
EMAIL_HOST_PASSWORD = '............'

DEFAULT_FROM_EMAIL = 'xxxx@gmail.com'

EMAIL_TIMEOUT = 10
