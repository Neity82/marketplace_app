from marketplace_app.settings import *


SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default='foo'
)
DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', default='').split(' ')

INSTALLED_APPS += (
    'discount.apps.DiscountConfig',
    'info.apps.InfoConfig',
    'order.apps.OrderConfig',
    'product.apps.ProductConfig',
    'shop.apps.ShopConfig',
    'user.apps.UserConfig',
)

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.getenv(
            'SQL_DATABASE',
            default=os.path.join(BASE_DIR, 'db.sqlite3')
        ),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]


# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/login/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
