from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    """Класс описывающий модель магазина"""
    name = models.CharField(
        verbose_name=_("name"),
        max_length=150
    )

    description = models.TextField(
        verbose_name=_("description"),
        blank=True
    )

    image = models.ImageField(
        verbose_name=_("image"),
        null=True,
        upload_to='shop_images/'
    )

    address = models.CharField(
        verbose_name=_("address"),
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        verbose_name=_("phone"),
        max_length=15,
        blank=True
    )

    mobile = models.CharField(
        verbose_name=_("mobile"),
        max_length=15,
        blank=True
    )

    email_general = models.EmailField(
        verbose_name=_("general email"),
        blank=True
    )

    email_editor = models.EmailField(
        verbose_name=_("editor email"),
        blank=True
    )

    shipping_policy = models.CharField(
        verbose_name=_("shipping and returns policy"),
        max_length=50,
        blank=True
    )

    refund_policy = models.CharField(
        verbose_name=_("refund policy"),
        max_length=50,
        blank=True
    )

    support_policy = models.CharField(
        verbose_name=_("support policy"),
        max_length=50,
        blank=True
    )

    quality_policy = models.CharField(
        verbose_name=_("quality policy"),
        max_length=50,
        blank=True
    )

    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        verbose_name = _("shop")
        verbose_name_plural = _("shops")

    def __str__(self):
        return "{name}".format(
            name=self.name
        )
