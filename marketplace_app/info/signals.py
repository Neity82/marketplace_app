from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver

from info.models import Banner


@receiver(post_save, sender=Banner)
def clear_banner_list_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("banner_list")
    cache.delete(key)
