from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Category, Product


@receiver(post_save, sender=Category)
def clear_category_list_cache(sender, instance, **kwargs):
    cache.delete('categories_list')


@receiver(post_save, sender=Product)
def clear_product_list_cache(sender, instance, **kwargs):
    cache.delete('product_list')
