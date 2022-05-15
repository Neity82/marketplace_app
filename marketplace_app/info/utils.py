import datetime
import os


def banner_image_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения баннера"""

    extension = os.path.splitext(filename)
    return f'banner/{datetime.datetime.now()}_{instance.title}.{extension}'
