from config.utils import load_secrets
from .base import *

env = 'local'

SECRET_DIR = os.path.join(os.path.join(os.path.dirname(BASE_DIR), '.secrets'), f'{env}_secrets.json')
secrets = load_secrets(env, SECRET_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

connection_info = secrets['DB_CONNECTION_INFO']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': connection_info['NAME'],
        'USER': connection_info['USER'],
        'PASSWORD': connection_info['PASSWORD'],
        'HOST': connection_info['HOST'],
        'PORT': connection_info['PORT'],
    }
}

# Google OAuth
google_oauth = secrets['GOOGLE_OAUTH']
GOOGLE_CLIENT_ID = google_oauth['CLIENT_ID']
GOOGLE_CLIENT_SECRET = google_oauth['CLIENT_SECRET']
