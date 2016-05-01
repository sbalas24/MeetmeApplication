"""
Django settings for meetme project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ej)+8i&zef^p5%k*lojuc8&mga01v(ebwlmj0zibeasa_g(-0k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'meetme.core',
    'meetme.users',
    'social_auth',
    'datetimewidget',
    'django_facebook',
    'filer',
    'easy_thumbnails',
    'calendarium',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware'
)

ROOT_URLCONF = 'meetme.urls'

HOME_PATH = '/Users/hacker/soham/django_apps/meetme/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['meetme/templates/',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
                'django_facebook.context_processors.facebook',
                # and add request if you didn't do so already
                'django.core.context_processors.request',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATES[0]['OPTIONS']['context_processors']

WSGI_APPLICATION = 'meetme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

URL = 'http://ec2-52-32-130-148.us-west-2.compute.amazonaws.com'

AUTHENTICATION_BACKENDS = (
        'social_auth.backends.google.GoogleOAuth2Backend',
        'social_auth.backends.google.GoogleBackend',
        'django.contrib.auth.backends.ModelBackend',
    'django_facebook.auth_backends.FacebookBackend',
        )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = '/static/'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     )
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'meetme/static'),
)

#Login With Google Sign in
GOOGLE_OAUTH2_CLIENT_ID      = '751005055062-g04uncrgss78cd717tshqedbm4m6mqd0.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = 'Jo1Qqp7WPvoWQkVeFBze3b7V'
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['primary','foo']

LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = LOGIN_URL
LOGIN_ERROR_URL    = LOGIN_URL

import random
SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])
GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}
SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/calendar.readonly']
GOOGLE_CALENDER_CREDENTIALS = {"web":{"client_id":"751005055062-g04uncrgss78cd717tshqedbm4m6mqd0.apps.googleusercontent.com","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"Jo1Qqp7WPvoWQkVeFBze3b7V","redirect_uris":["http://localhost:8000/complete/google-oauth2/"],"javascript_origins":["http://localhost:8000"]}}
GOOGLE_CALENDAR_EVENT_API = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'


FACEBOOK_APP_ID = '1643059665962235'
FACEBOOK_APP_SECRET = '67b99776cfa6a0231c21d459b9218b2a'
# AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'
AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'
FACEBOOK_DEFAULT_SCOPE = ['email','public_profile','user_friends','user_events']
FACEBOOK_USER_DATA_URL = 'https://graph.facebook.com/v2.5/me'
FACEBOOK_USER_EVENTS_URL=FACEBOOK_USER_DATA_URL+'?fields=events{id,description,end_time,name,start_time}'

# MEETME_FROM_EMAIL = 'soham.art90@gmail.com'
# EMAIL_HOST = 'smtp.mandrillapp.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'sshirgao@asu.edu'
# EMAIL_HOST_PASSWORD = 'aFA2dP4VhCdZba4HXxaAgA'

MEETME_FROM_EMAIL = 'Meetme<vinothkumar.raja@asu.edu>'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'vinothkumar.raja@asu.edu'
EMAIL_HOST_PASSWORD = 'Y8avc-_RNKUIfEQGMf0jRg'



UNSUB_LINK = URL+'/editProfile/?ep=hey'