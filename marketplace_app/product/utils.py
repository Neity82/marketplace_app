import os.path

import datetime
import random


def category_icon_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения категории"""

    extension = os.path.splitext(filename)
    return f'category/{datetime.datetime.now()}_{instance.title}.{extension}'


def product_image_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения товара"""

    extension = os.path.splitext(filename)
    return f'product/{datetime.datetime.now()}_{instance.title}.{extension}'


def get_random_item(qs, count):
    qs_count = qs.count()
    index_list = range(qs_count)
    if qs_count >= count:
        index_list = random.sample(index_list, count)
    else:
        index_list = random.sample(index_list, qs_count)
    item_list = [qs[i] for i in index_list]
    return item_list
