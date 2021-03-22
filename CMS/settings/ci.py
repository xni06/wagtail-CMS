from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# NOTE: this SECRET_KEY is ONLY used in testing, NOT used in production
SECRET_KEY = 'secret-key-for-testing'

# used by Github Actions because you can't set environement variables
DBHOST = 'localhost'
DBNAME = 'django'
DBUSER = 'docker'
DBPASSWORD = 'docker'
DBPORT = '5432'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': DBHOST,
        'NAME': DBNAME,
        'USER': DBUSER,
        'PASSWORD': DBPASSWORD,
        'PORT': DBPORT
    }
}

MONGODB_HOST = 'localhost'
MONGODB_USERNAME = 'mongodb'
MONGODB_PASSWORD = 'mongodb'
