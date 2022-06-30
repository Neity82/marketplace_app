from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Shop


@receiver(post_save, sender=Shop)
def clear_cache(sender, instance, **kwargs):
    cache.delete("shop_info")
