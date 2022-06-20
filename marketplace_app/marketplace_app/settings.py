"""
Django dev_settings for marketplace_app project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of dev_settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development dev_settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4(r-gu$)q!a3%wf!pv#6y2$%=)%3fgguhlx%sn(jw3l-)7_t)t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'discount.apps.DiscountConfig',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'info.apps.InfoConfig',
    'order.apps.OrderConfig',
    'product.apps.ProductConfig',
    'shop.apps.ShopConfig',
    'user.apps.UserConfig',
    # 'modeltranslation',
    # 'django_celery_beat',
    'import_export_celery',
    'import_export',
    'payments.apps.PaymentsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
]

ROOT_URLCONF = 'marketplace_app.urls'

TEMPLATES_PRODUCT_DIR = os.path.join(BASE_DIR, "product", "templates")
TEMPLATES_INFO_DIR = os.path.join(BASE_DIR, "info", "templates")
TEMPLATES_DISCOUNT_DIR = os.path.join(BASE_DIR, "discount", "templates")
TEMPLATES_ORDER_DIR = os.path.join(BASE_DIR, "order", "templates")
TEMPLATES_SHOP_DIR = os.path.join(BASE_DIR, "shop", "templates")
TEMPLATES_USER_DIR = os.path.join(BASE_DIR, "user", "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            TEMPLATES_PRODUCT_DIR,
            TEMPLATES_INFO_DIR,
            TEMPLATES_DISCOUNT_DIR,
            TEMPLATES_ORDER_DIR,
            TEMPLATES_SHOP_DIR,
            TEMPLATES_USER_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'info.views.seo_data',
                'order.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'marketplace_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_DISCOUNT_DIR = os.path.join(BASE_DIR, "discount", "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    STATIC_DISCOUNT_DIR,
]

STATIC_DISCOUNT_DIR = os.path.join(BASE_DIR, "discount", "static")

STATICFILES_DIRS += [STATIC_DISCOUNT_DIR]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.CustomUser'

# LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/login/'

# REDIS related settings
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

IMPORT_EXPORT_CELERY_INIT_MODULE = "marketplace_app.celery"

IMPORT_EXPORT_CELERY_MODELS = {
    "Stock": {
        'app_label': 'stock',
        'model_name': 'Stock',
    }
}

