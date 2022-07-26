import datetime
import os
from typing import Union

from django.urls import URLResolver, get_resolver, URLPattern

DEFAULT_CACHE_TIME = 30000


def banner_image_path(instance, filename) -> str:
    """Функция формирует путь для размещения изображения баннера"""

    extension = os.path.splitext(filename)
    return f"banner/{datetime.datetime.now()}_{instance.title}.{extension}"


def get_urls(resolver: Union[str, URLResolver] = None, namespace=None):
    if not resolver:
        resolver = get_resolver()
    if isinstance(resolver, str):
        resolver = get_resolver(resolver)

    if resolver.namespace and namespace:
        namespace = f"{namespace}:{resolver.namespace}"
    result_list = []
    for item in resolver.url_patterns:
        if isinstance(item, URLPattern):
            if (
                item.name is None
                or not resolver.namespace
                or resolver.namespace.startswith("admin")
            ):
                continue
            result_list.append(f"{namespace or resolver.namespace}:{item.name}")
        elif isinstance(item, URLResolver):
            result_list.extend(get_urls(item, namespace=resolver.namespace))

    return result_list
