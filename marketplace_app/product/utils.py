import os.path

import datetime

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect


def category_icon_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения категории"""

    extension = os.path.splitext(filename)
    return f'category/{datetime.datetime.now()}_{instance.title}.{extension}'


def product_image_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения товара"""

    extension = os.path.splitext(filename)
    return f'product/{datetime.datetime.now()}_{instance.product.title}.{extension}'


def undelete_admin(admin_model: admin.ModelAdmin, request: WSGIRequest, obj):
    print(type(request))
    print(type(obj))
    if "_undelete" in request.POST:
        obj.deleted_at = None
        obj.save()
        print(obj)
        admin_model.message_user(request, f"This {obj} is indeleted")
        return HttpResponseRedirect(".")
