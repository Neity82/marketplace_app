from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InfoConfig(AppConfig):
    name = "info"
    verbose_name = _("info")
    verbose_name_plural = _("info")
    default_auto_field = "django.db.models.BigAutoField"
