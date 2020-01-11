from config.utils import load_secrets

from .base import *

env = 'test'

SECRET_DIR = os.path.join(os.path.join(os.path.dirname(BASE_DIR), '.secrets'), f'{env}_secrets.json')
secrets = load_secrets(env, SECRET_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

connection_info = secrets['DB_CONNECTION_INFO']
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
