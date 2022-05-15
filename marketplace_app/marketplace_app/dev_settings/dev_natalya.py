import os

import environ

from marketplace_app.settings import *

env = environ.Env()
environ.Env.read_env()
ALLOWED_HOSTS = ["*"]
DEBUG = env.get_value('DEBUG')
SECRET_KEY = env.get_value('SECRET_KEY')

# INSTALLED_APPS += (
#     'debug_toolbar',
#     'info.apps.InfoConfig',
#     'order.apps.OrderConfig',
#     'product.apps.ProductConfig',
#     'shop.apps.ShopConfig',
#     'user.apps.UserConfig',
# )

# MIDDLEWARE += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )


DATABASES = {
    'default': {
        'ENGINE': env.get_value('DB_ENGINE'),
        'NAME': env.get_value('DB_NAME'),
        'USER': env.get_value('DB_USER'),
        'PASSWORD': env.get_value('DB_PASSWORD'),
        'HOST': env.get_value('DB_HOST'),
        'PORT': env.get_value('DB_PORT'),
    }
}

LANGUAGE_CODE = 'ru'

STATIC_URL = '/static/'

# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/login/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

INTERNAL_IPS = [
    '127.0.0.1',
]

import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
