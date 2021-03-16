from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# NOTE: this SECRET_KEY is ONLY used in testing, NOT used in production
SECRET_KEY = 'secret-key-for-testing'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'django',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'PORT': '5432'
    }
}

MONGODB_HOST = 'localhost'
MONGODB_USERNAME = 'mongodb'
MONGODB_PASSWORD = 'mongodb'
