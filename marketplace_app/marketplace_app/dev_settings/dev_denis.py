from marketplace_app.settings import *
import environ

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
    }
}