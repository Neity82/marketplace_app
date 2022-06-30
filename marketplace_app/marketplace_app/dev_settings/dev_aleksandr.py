import sys

import environ

from marketplace_app.settings import *

env = environ.Env()
environ.Env.read_env()
ALLOWED_HOSTS = ["*"]
DEBUG = env.get_value('DEBUG')
SECRET_KEY = env.get_value('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': env.get_value('DB_ENGINE'),
        'NAME': env.get_value('DB_NAME'),
        'USER': env.get_value('DB_USER'),
        'PASSWORD': env.get_value('DB_PASSWORD'),
        'HOST': env.get_value('DB_HOST'),
        'PORT': env.get_value('DB_PORT'),
        'TEST': {
            'NAME': f'test_{env.get_value("DB_NAME")}',
            'USER': env.get_value('DB_USER'),
        },
    }

}

STATIC_URL = '/static/'

STATIC_ROOT = ''

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if sys.argv[1] == 'test':
    print('Run bin/django_db.sh if permission denied to create database')
elif sys.argv[1] == 'runserver':
    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'fixtures'),)

# обещаю так больше не делать
print(f'Current DB: {DATABASES["default"]["NAME"]}')
