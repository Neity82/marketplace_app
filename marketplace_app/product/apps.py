from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    verbose_name = _("Product")
    verbose_name_plural = _("Products")

    def ready(self):
        from . import signals
