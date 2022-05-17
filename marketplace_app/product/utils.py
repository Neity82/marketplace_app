import os.path

import datetime


def category_icon_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения категории"""

    extension = os.path.splitext(filename)
    return f'category/{datetime.datetime.now()}_{instance.title}.{extension}'


def product_image_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения товара"""

    extension = os.path.splitext(filename)
    return f'product/{datetime.datetime.now()}_{instance.title}.{extension}'

