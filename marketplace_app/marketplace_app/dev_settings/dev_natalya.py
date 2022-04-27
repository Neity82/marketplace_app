import os

import environ

from marketplace_app.settings import *

env = environ.Env()
environ.Env.read_env()
ALLOWED_HOSTS = ["*"]
DEBUG = env.get_value('DEBUG')
SECRET_KEY = env.get_value('SECRET_KEY')

# INSTALLED_APPS += (
#     'discount.apps.DiscountConfig',
#     'info.apps.InfoConfig',
#     'order.apps.OrderConfig',
#     'product.apps.ProductConfig',
#     'shop.apps.ShopConfig',
#     'user.apps.UserConfig',
# )


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

