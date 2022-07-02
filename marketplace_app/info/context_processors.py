from django.core.handlers.wsgi import WSGIRequest

from info.models import Settings
from info.utils import DEFAULT_CACHE_TIME


def cache_time(request: WSGIRequest) -> dict:
    category_cache = Settings.objects.filter(name="category_list_cache_time").first()
    product_cache = Settings.objects.filter(name="product_list_cache_time").first()
    return {
        "category_list_cache_time": category_cache.value
        if category_cache
        else DEFAULT_CACHE_TIME,
        "product_list_cache_time": product_cache.value
        if product_cache
        else DEFAULT_CACHE_TIME,
    }