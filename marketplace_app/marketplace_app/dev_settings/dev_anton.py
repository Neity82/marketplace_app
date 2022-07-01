import os
from marketplace_app.settings import *


SECRET_KEY = os.getenv("SECRET_KEY", default="foo")
DEBUG = os.getenv("DEBUG", default=False)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", default="").split(" ")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": os.getenv(
            "SQL_DATABASE", default=os.path.join(BASE_DIR, "db.sqlite3")
        ),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }

REDIS_HOST = "redis"
