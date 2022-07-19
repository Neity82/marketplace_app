import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from order.models import Order


class Payment(models.Model):
    """Модель платежа"""

    class Status(models.TextChoices):
        PROCESSING = "processing", _("Processing")
        CANCELED = "canceled", _("Canceled")
        SUCCESS = "success", _("Success")
        ERROR = "error", _("Error")

    uuid = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payment",
        verbose_name=_("order"),
    )
    card = models.CharField(
        _("card number"),
        max_length=9,
    )
    status = models.CharField(
        _("status"),
        max_length=150,
        choices=Status.choices,
        default=Status.PROCESSING.value,
    )
    message = models.CharField(
        _("message"),
        max_length=255,
        blank=True,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )

    class Meta:
        ordering = ("order", "created_at")
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return _("{model} for {order}").format(
            model=self._meta.verbose_name.title(),
            order=self.order,
        )

    @property
    def id(self):
        return self.uuid
