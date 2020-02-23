import os
from decouple import config
from django.urls import reverse, reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


THIRD_PARTY_APPS = [
    'crispy_forms',
    'bootstrap4',

]

PROJECT_APPS = [
    'inqoire.users.apps.UsersConfig',
    'inqoire.answer.apps.AnswerConfig',
    'inqoire.question.apps.QuestionConfig',
    'inqoire.comment.apps.CommentConfig',
    'inqoire.connection.apps.ConnectionConfig',
    'inqoire.contribute.apps.ContributeConfig',
    'inqoire.vote.apps.VoteConfig',
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'inqoire.account.middleware.RestrictUserToAdminRouteMiddleware',
    'inqoire.account.middleware.LastIPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'inqoire.account.context_processors.is_auth',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'inqoire.account.authenticate.EmailorUserNameAuthBackend',
# )


AUTH_USER_MODEL = 'users.User'


# App Account Access
LOGIN_REDIRECT_URL = reverse_lazy('/') # not redirecting using redirect(settings.LOGIN_REDIRECT_URL)
LOGIN_URL = reverse_lazy('account:login')
LOGOUT_URL = reverse_lazy('/')

# Congif.
ACCOUNT_ACTIVATION_REQUIRED = True

# Message Tags.
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media') 

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static','static_env')]

STATIC_ROOT = os.path.join(BASE_DIR,'static','static_cdn')



# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Avatar
RANDOM_AVATAR_PATH = os.path.join(MEDIA_ROOT,'random_avatars') 


# inQoire config. for account activate
# True - Email Activation will be required
ALLOW_CONFIRMATION = False


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = { 
    'version': 1,
    'disable_existing_loggers': False,
    'filters':{
        'require_debug_false':{
            '()':'django.utils.log.RequireDebugFalse',
        },
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

