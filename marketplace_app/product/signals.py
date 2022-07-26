from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import Category, Product, ProductImage
from user.models import UserProductView


@receiver(post_save, sender=Category)
def clear_category_list_cache(sender, instance, **kwargs):
    for key_string in list(cache._cache.keys()):
        _, _, cache_key = key_string.split(sep=":")
        if "category_list" in cache_key:
            cache.delete(cache_key)


@receiver(post_save, sender=[Product, ProductImage])
def clear_product_list_cache(sender, instance, **kwargs):
    for key_string in list(cache._cache.keys()):
        _, _, cache_key = key_string.split(sep=":")
        if "product_list_" in cache_key:
            cache.delete(cache_key)
    key = make_template_fragment_key("product_detail_cache")
    cache.delete(key)
    key = make_template_fragment_key("top_product_list")
    cache.delete(key)


get_product_detail_view = Signal()


@receiver(get_product_detail_view)
def add_product_view(**kwargs):
    UserProductView.add_object(user=kwargs["user"], product=kwargs["product"])
