from django.db import models
from django.utils.translation import gettext_lazy as _


class Discount(models.Model):
    class Meta:
        verbose_name = _("discount")
        verbose_name_plural = _("discounts")

    class DiscountType(models.TextChoices):
        PRODUCT_DISCOUNT = "PD", _("Product discount")
        # SET_DISCOUNT = "SD", _("Set discount")
        BASKET_DISCOUNT = "BD", _("Basket discount")

    discount_type = models.CharField(
        verbose_name=_("discount type"),
        help_text=_("Discount type"),
        max_length=2,
        choices=DiscountType.choices,
        default=DiscountType.PRODUCT_DISCOUNT,
    )

    class DiscountMechanism(models.TextChoices):
        PERCENT = "P", _("Percent discount")
        DISCOUNT_SUM = "S", _("Discount sum")
        FIX_PRICE = "F", _("Fix price")

    discount_mechanism = models.CharField(
        verbose_name=_("discount mechanism"),
        help_text=_("Discount mechanism"),
        max_length=1,
        choices=DiscountMechanism.choices,
        default=DiscountMechanism.PERCENT,
    )

    discount_value = models.PositiveIntegerField(
        verbose_name=_("discount value"),
        help_text=_("Discount value"),
        default=0,
    )

    is_active = models.BooleanField(
        verbose_name=_("is active"),
        help_text=_("There is active discount"),
        default=True,
    )

    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Discount description"),
        max_length=1000,
    )

    start_at = models.DateTimeField(
        verbose_name=_("start at"),
        help_text=_("Discount start date"),
    )

    finish_at = models.DateTimeField(
        verbose_name=_("finish at"),
        help_text=_("Discount finish date"),
        blank=True,
        null=True,
        default=None,
    )

    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.description}"


class ProductDiscount(models.Model):
    class Meta:
        verbose_name = _("product discount")
        verbose_name_plural = _("product discounts")

    discount_id = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="product_discount",
        verbose_name=_("discount id"),
        help_text=_("Discount id"),
    )

    product_id = models.ManyToManyField(
        "product.Product",
        verbose_name=_("product(s) id"),
        help_text=_("Product(s) id"),
        related_name="product_discount",
        blank=True,
        default="",
    )

    category_id = models.ManyToManyField(
        "product.Category",
        verbose_name=_("category(ies) id"),
        help_text=_("Category(ies) id"),
        related_name="product_discount",
        blank=True,
        default="",
    )

    objects = models.Manager()


class SetDiscount(models.Model):
    class Meta:
        verbose_name = _("set discount")
        verbose_name_plural = _("set discounts")

    discount_id = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="set_discount",
        verbose_name=_("discount id"),
        help_text=_("Discount id"),
    )

    product_id_1 = models.ManyToManyField(
        "product.Product",
        verbose_name=_("product(s) 1 id"),
        help_text=_("Product(s) 1 id"),
        related_name="set_discount_1",
        blank=True,
        default="",
    )

    category_id_1 = models.ManyToManyField(
        "product.Category",
        verbose_name=_("category(ies) 1 id"),
        help_text=_("Category(ies) 1 id"),
        related_name="set_discount_1",
        blank=True,
        default="",
    )

    product_id_2 = models.ManyToManyField(
        "product.Product",
        verbose_name=_("product(s) 2 id"),
        help_text=_("Product(s) 2 id"),
        related_name="set_discount_2",
        blank=True,
        default="",
    )

    category_id_2 = models.ManyToManyField(
        "product.Category",
        verbose_name=_("category(ies) 2 id"),
        help_text=_("Category(ies) 2 id"),
        related_name="set_discount_2",
        blank=True,
        default="",
    )


class BasketDiscount(models.Model):
    class Meta:
        verbose_name = _("basket discount")
        verbose_name_plural = _("basket discounts")

    discount_id = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="basket_discount",
        verbose_name=_("discount id"),
        help_text=_("Discount id"),
    )

    min_products_count = models.PositiveIntegerField(
        verbose_name=_("minimum products count"),
        help_text=_("Minimum products count"),
        default=0,
    )

    max_products_count = models.PositiveIntegerField(
        verbose_name=_("maximum products count"),
        help_text=_("Maximum products count"),
        default=0,
    )

    min_basket_cost = models.PositiveIntegerField(
        verbose_name=_("minimum basket cost"),
        help_text=_("Minimum basket cost"),
        default=0,
    )

    max_basket_cost = models.PositiveIntegerField(
        verbose_name=_("maximum basket cost"),
        help_text=_("Maximum basket cost"),
        default=0,
    )
