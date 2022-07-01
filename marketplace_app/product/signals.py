from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal


from .models import Category, Product
from user.models import UserProductView


@receiver(post_save, sender=Category)
def clear_category_list_cache(sender, instance, **kwargs):
    cache.delete('categories_list')


@receiver(post_save, sender=Product)
def clear_product_list_cache(sender, instance, **kwargs):
    cache.delete('product_list')


get_product_detail_view = Signal()


@receiver(get_product_detail_view)
def add_product_view(**kwargs):
    UserProductView.add_object(
        user=kwargs["user"],
        product=kwargs["product"]
    )
