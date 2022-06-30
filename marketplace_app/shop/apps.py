from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    name = "shop"
    verbose_name = _("Shop")
    verbose_name_plural = _("Shops")
<<<<<<< HEAD
    default_auto_field = "django.db.models.BigAutoField"
=======
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import signals
>>>>>>> 1797d9f1756005ab8f257a6239f444f0c0e947d6
