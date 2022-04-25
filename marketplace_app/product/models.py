from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import category_icon_path, product_image_path


class Tag(models.Model):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Tag title"),
        max_length=50,
    )

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    parent_id = models.BigIntegerField(
        verbose_name=_("parent id"),
        help_text=_("Parent category id"),
        null=True,
        default=None,
    )

    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Category title"),
        max_length=50,
    )

    icon = models.ImageField(
        verbose_name=_("icon"),
        help_text=_("Categiry icon"),
        null=True,
        default=None,
        upload_to=category_icon_path,
    )

    def __str__(self) -> str:
        parent_title = (
            ""
            if self.parent_id is None
            else Category.objects.get(id=self.parent_id).__str__() + "->"
        )
        return parent_title + self.title


class Product(models.Model):
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Product  title"),
        max_length=150,
    )

    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Product image"),
        upload_to=product_image_path,
    )

    short_description = models.CharField(
        verbose_name=_("short description"),
        help_text=_("Product short description"),
        max_length=150,
    )

    long_description = models.CharField(
        verbose_name=_("long description"),
        help_text=_("Product long description"),
        max_length=150,
    )

    is_limited = models.BooleanField(
        verbose_name=_("is limited"),
        help_text=_("There is limited edition"),
        default=False,
    )

    tag_id = models.ManyToManyField(
        Tag,
        related_name="product",
        blank=True,
        default="",
    )

    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name=_("category"),
        help_text=_("Product category"),
    )

    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("Date the product was added"),
        auto_now_add=True,
    )

    class Rating(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    rating = models.PositiveSmallIntegerField(
        verbose_name=_("rating"),
        help_text=_("Product rating"),
        choices=Rating.choices,
        default=Rating.ZERO,
    )
