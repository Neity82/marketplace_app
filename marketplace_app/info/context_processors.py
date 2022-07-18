from django.core.handlers.wsgi import WSGIRequest

from info.models import Settings
from info.utils import DEFAULT_CACHE_TIME


def cache_time(request: WSGIRequest) -> dict:
    top_product_cache = Settings.objects.filter(name="top_product_list_cache_time").first()
    banner_cache = Settings.objects.filter(name="banner_list_cache_time").first()

    return {
        "top_product_list_cache_time": top_product_cache.value if top_product_cache else DEFAULT_CACHE_TIME,
        "banner_list_cache_time": banner_cache.value if banner_cache else DEFAULT_CACHE_TIME
    }
