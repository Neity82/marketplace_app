from info.models import Settings


def cache_time(request) -> dict:
    return {
        'category_list_cache_time':
            Settings.objects.get(name='category_list_cache_time').value,
        'product_list_cache_time':
            Settings.objects.get(name='product_list_cache_time').value
    }
