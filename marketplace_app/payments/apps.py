from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentsConfig(AppConfig):
    name = "payments"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("payment")
    verbose_name_plural = _("payments")
