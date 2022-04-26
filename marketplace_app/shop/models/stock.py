from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _

from .shop import Shop


Product = apps.get_model(app_label='product', model_name='Product')


class Stock(models.Model):
    shop = models.OneToOneField(
        Shop,
        on_delete=models.CASCADE,
        related_name='stock',
        verbose_name=_("shop"),
        primary_key=True,
    )
    entities = models.ManyToManyField(
        Product,
        related_name='stocks',
        through='StockEntity',
        through_fields=('stock', 'product'),
        verbose_name=_("entities"),
    )

    class Meta:
        ordering = ('shop',)
        verbose_name = _("stock")
        verbose_name_plural = _("stocks")

    def __str__(self):
        return "{shop}".format(
            shop=self.shop
        )


class StockEntity(models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='stock_entity',
        verbose_name=_("stock"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_entity',
        verbose_name=_("product"),
    )
    quantity = models.PositiveSmallIntegerField(_("quantity"))
    price = models.DecimalField(
        _("price"),
        max_digits=11,
        decimal_places=2,
        help_text=_("The price cannot be more than 999 999 999 and 99.")
    )

    class Meta:
        ordering = ('stock',)
        verbose_name = _("stock entity")
        verbose_name_plural = _("stock entities")

    def __str__(self):
        return _("Entity of {stock}").format(
            stock=self.stock
        )
