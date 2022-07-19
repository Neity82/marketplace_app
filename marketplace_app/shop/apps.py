from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    name = "shop"
    verbose_name = _("shop")
    verbose_name_plural = _("shops")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import signals
