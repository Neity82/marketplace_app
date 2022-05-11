from marketplace_app.settings import *
# INSTALLED_APPS += (
#     'discount.apps.DiscountConfig',
#     'info.apps.InfoConfig',
#     'order.apps.OrderConfig',
#     'product.apps.ProductConfig',
#     'shop.apps.ShopConfig',
#     'user.apps.UserConfig',
# )

# DATABASES = {
#     'default': {
#         'ENGINE': env.get_value('DB_ENGINE'),
#         'NAME': env.get_value('DB_NAME'),
#         'USER': env.get_value('DB_USER'),
#         'PASSWORD': env.get_value('DB_PASSWORD'),
#         'HOST': env.get_value('DB_HOST'),
#         'PORT': env.get_value('DB_PORT'),
#     }
# }

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# LOGIN_URL = '/login/'
# LOGIN_REDIR

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'