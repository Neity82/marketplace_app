from __future__ import annotations
from datetime import date, datetime
import pytz
from decimal import Decimal
from typing import List, Optional, TypedDict, Union

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q, Avg, Min, Sum, QuerySet
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from timestamps.models import SoftDeletes

from discount.models import Discount
from discount.models import ProductDiscount
from shop.models import Shop
from .utils import category_icon_path, product_image_path


class Tag(models.Model):
    """Модель: тэг"""

    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("tag title"),
        max_length=50,
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self) -> str:
        return getattr(self, "title")


class Category(SoftDeletes):
    """Модель: категория"""

    SEP = " / "

    parent = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name=_("parent id"),
        related_name="child",
        help_text=_("parent category"),
        null=True,
        blank=True,
        default=None,
    )

    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("category title"),
        max_length=50,
    )

    icon = models.ImageField(
        verbose_name=_("icon"),
        help_text=_("category icon"),
        null=True,
        default=None,
        upload_to=category_icon_path,
    )

    sort_index = models.SmallIntegerField(
        verbose_name=_("sort index"),
        help_text=_("sort index"),
        default=0
    )

    admin_objects = models.Manager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self) -> str:
        return self.get_category_recur()

    def get_category_recur(self) -> str:
        """Рекурсивно получаем тайтлы категорий и их родителей"""
        title = getattr(self, "title")
        parent = getattr(self, "parent")
        return (f"{parent.get_category_recur()}{self.SEP}{title}"
                if parent else title)

    @classmethod
    def get_popular(cls, limit: int = 3) -> QuerySet[Product]:
        """
        Метод для получения n избранных категорий товаров

        :param limit: Необходимое количество категорий
        :type limit: int
        :return: Список объектов категорий
        :rtype: QuerySet[Category]
        """

        queryset: QuerySet[Product] = Category.objects.prefetch_related(
            "product"
        ).filter(
            product__stock__count__gt=0,
        ).distinct().annotate(
            min_price=Min("product__stock__price"),
            selling=Coalesce(
                Sum("product__stock__order_entity_stock__count"),
                0
            )
        ).order_by(
            "-sort_index",
            "-selling"
        )

        return queryset[:limit]


class Unit(models.Model):
    """Модель: Единица измерения для атрибута"""
    title = models.CharField(
        max_length=16,
        verbose_name=_("unit title"),
        blank=False,
        null=False,
    )
    unit_description = models.CharField(
        max_length=128,
        verbose_name=_("unit description"),
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("unit")
        verbose_name_plural = _("units")

    def __str__(self) -> str:
        return getattr(self, "title")


class Attribute(models.Model):
    """
    Модель: характеристика
    """
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Category title"),
        max_length=50,
    )

    class AttributeType(models.TextChoices):
        TEXT = "T", _("text")
        CHECK = "C", _("check")
        SELECT = "S", _("select")

    type = models.CharField(
        verbose_name=_("field type"),
        max_length=1,
        help_text=_("field type"),
        choices=AttributeType.choices,
        default=AttributeType.TEXT
    )

    category = models.ForeignKey(
        "Category",
        verbose_name=_("'attribute\'s category'"),
        related_name="attribute",
        on_delete=models.CASCADE,
    )

    rank = models.IntegerField(
        default=0,
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ],
        help_text=_("Rank of importance. 100 - most important"),
    )

    help_text = models.CharField(max_length=150)
    objects = models.Manager()

    class Meta:
        verbose_name = _("attribute")
        verbose_name_plural = _("attribute")

    def __str__(self) -> str:
        return getattr(self, "title")


class AttributeValue(models.Model):
    """
    Модель: значение характеристики
    """
    value = models.CharField(
        max_length=255,
        verbose_name=_("value"),
        null=True,
        default=None
    )

    unit = models.ForeignKey(
        "Unit",
        verbose_name=_("unit"),
        related_name="value_unit",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    attribute = models.ForeignKey(
        "Attribute",
        verbose_name=_("'product\'s attribute'"),
        related_name="product_attribute",
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        "Product",
        verbose_name=_("product item"),
        related_name="product_item",
        on_delete=models.CASCADE,
        default=None,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("attribute value")
        verbose_name_plural = _("attribute values")

    def __str__(self) -> str:
        return str(getattr(self, "value"))

    objects = models.Manager()

    @classmethod
    def get_all_attributes_of_product(cls, product: Product) \
            -> QuerySet[AttributeValue]:
        return AttributeValue.objects.filter(product=product)\
                                     .order_by("-attribute__rank")


DiscountDict = TypedDict(
        "DiscountDict",
        {
            "type": Optional[str],
            "value": Optional[int],
            "price": Optional[Decimal],
            "base": Optional[Decimal],
        }
    )


class Product(SoftDeletes):
    """Модель: продукт"""

    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("product title"),
        max_length=150,
    )

    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("product image"),
        upload_to=product_image_path,
        blank=True,
    )

    short_description = models.CharField(
        verbose_name=_("short description"),
        help_text=_("product short description"),
        max_length=150,
    )

    long_description = models.TextField(
        verbose_name=_("long description"),
        help_text=_("product long description"),
        max_length=1500,
    )

    is_limited = models.BooleanField(
        verbose_name=_("is limited"),
        help_text=_("there is limited edition"),
        default=False,
    )

    tags = models.ManyToManyField(
        "Tag",
        related_name="products",
        related_query_name="product",
        blank=True,
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name=_("category"),
        help_text=_("product category"),
    )

    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date the product was added"),
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
        help_text=_("product rating"),
        choices=Rating.choices,
        default=Rating.ZERO,
    )

    sort_index = models.SmallIntegerField(
        verbose_name=_("sort index"),
        help_text=_("sort index"),
        default=0
    )

    admin_objects = models.Manager()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("product")

    def __str__(self) -> str:
        category = getattr(self, "category", None)
        return (
            f"({getattr(category, 'title')}) {getattr(self, 'title')}"
            if category
            else f"{getattr(self, 'title')}"
        )

    @property
    def _price(self) -> Optional['Decimal']:
        """Метод для получения средней цены

        :return: Значение средней цены
        :rtype: Optional[Decimal]
        """
        avg_price = Stock.objects.filter(
            product=self.pk,
            count__gt=0
        ).aggregate(avg=Avg("price"))["avg"]
        if avg_price is None:
            return None
        return Decimal(round(avg_price, 2))

    def _get_discounted_price(
            self, base_price: 'Decimal', discount: 'Discount'
    ) -> Decimal:
        """Метод получения скидочной цены

        :param base_price: Базовая цена
        :type base_price: Decimal
        :param discount: Объект скидки
        :type discount: Discount
        :return: Скидочная стоимость
        :rtype: Decimal
        """
        if discount.discount_mechanism == "P":
            return Decimal(
                round(
                    (
                            base_price *
                            (100 - discount.discount_value) / 100
                    ),
                    2
                )
            )
        elif discount.discount_mechanism == "S":
            result: Decimal = (
                Decimal(
                    round((base_price - discount.discount_value), 2)
                )
                if base_price - discount.discount_value >= 1
                else Decimal("1.00")
            )
            return result
        elif discount.discount_mechanism == "F":
            return Decimal(discount.discount_value)
        return Decimal("NaN")

    @property
    def discount(self) -> DiscountDict:
        """Свойство для хранения механизма скидки и скидочной стоимости

        :return: Словарь с механизмом скидки и скидочной стоимостью
        :rtype: Dict[str, Union[str, Decimal]]
        """
        base_price: Optional['Decimal'] = self._price
        result: DiscountDict = {
            "type": None,
            "value": None,
            "price": base_price,
            "base": base_price
        }
        if base_price is None:
            return result
        today: datetime = pytz.UTC.localize(datetime.today())
        categories_list: list = [self.category_id]
        if self.category.parent_id is not None:
            categories_list += [self.category.parent_id]
        discounts: QuerySet[ProductDiscount] = ProductDiscount.objects \
            .select_related("discount_id").filter(
            (
                Q(
                    product_id=self,
                    discount_id__discount_type="PD",
                    discount_id__is_active=True
                ) | Q(
                    category_id__in=categories_list,
                    discount_id__discount_type="PD",
                    discount_id__is_active=True
                )
            ) & (
                Q(
                    discount_id__start_at__lte=today,
                    discount_id__finish_at=None
                ) | Q(
                    discount_id__start_at__lte=today,
                    discount_id__finish_at__gt=today
                )
            )
        )
        if not discounts:
            return result
        discount_percent: QuerySet[ProductDiscount] = discounts.filter(
            discount_id__discount_mechanism="P"
        ).order_by(
            "-discount_id__discount_value"
        ).first()
        discount_sum: QuerySet[ProductDiscount] = discounts.filter(
            discount_id__discount_mechanism="S"
        ).order_by(
            "-discount_id__discount_value"
        ).first()
        discount_fix: QuerySet[ProductDiscount] = discounts.filter(
            discount_id__discount_mechanism="F"
        ).order_by(
            "discount_id__discount_value"
        ).first()
        max_discount_list = [
            discount_percent,
            discount_sum,
            discount_fix
        ]
        for obj in max_discount_list:
            if obj is None:
                continue
            discounted_price: Decimal = self._get_discounted_price(
                base_price, obj.discount_id
            )
            if discounted_price < result["price"]:
                result["type"] = obj.discount_id.discount_mechanism
                result["price"] = discounted_price
                result["value"] = obj.discount_id.discount_value
        return result

    @classmethod
    def get_popular(cls, shop: Union[Shop, None] = None, limit: int = 8) -> \
            QuerySet[Product]:
        """
        Метод для получения списка популярных товаров в количестве limit.
        Популярность определяется сначала по "индексу сортировки",
        если "индекс сортировки" одинаковый, тогда по количеству продаж

        :param shop: Объект shop
        :type shop: Union[Shop, None]
        :param limit: Необходимое количество товаров
        :type limit: int
        :return: Список товаров
        :rtype: QuerySet[Product]
        """

        queryset: QuerySet[Product] = Product.objects.prefetch_related(
            "stock"
        ).filter(
            stock__count__gt=0
        ).distinct().annotate(
            avg_price=Avg("stock__price"),
            selling=Coalesce(Sum("stock__order_entity_stock__count"), 0)
        ).order_by(
            "sort_index",
            "selling"
        )

        if shop:
            queryset = queryset.filter(stock__shop=shop)

        return queryset[:limit]

    def get_shops(self):
        return Shop.objects.filter(stock__product__id=self.pk)\
                           .only("name", "id")

    @classmethod
    def get_limited_edition(
            cls,
            daily_offer: Union[DailyOffer, None] = None,
            limit: int = 16
    ) -> QuerySet[Product]:
        """
        Метод для получения списка товаров ограниченного тиража

        :param daily_offer: Товар дня
        :type daily_offer: DailyOffer
        :param limit: Необходимое количество товаров
        :type limit: int
        :return: Список товаров
        :rtype: QuerySet[Product]
        """

        queryset: QuerySet[Product] = Product.objects.prefetch_related(
            "stock"
        ).filter(
            is_limited=True, stock__count__gt=0
        ).distinct().annotate(
            avg_price=Avg("stock__price")
        ).order_by("?").select_related("category__parent")

        if daily_offer:
            queryset = queryset.exclude(
                id=daily_offer.product_id)

        return queryset[:limit]

    @classmethod
    def get_product_with_discount(cls, limit: int = 9) -> List[Product]:
        """
        Метод для получения списка случайных товаров,
        на которые действует какая-нибудь акция в количестве limit

        :param limit: Необходимое количество товаров
        :type limit: int
        :return: Список товаров
        :rtype: List[Product]
        """

        queryset: List[Product] = Product.objects.prefetch_related(
            "stock",
            "product_discount"
        ).filter(
            stock__count__gt=0,
            product_discount__discount_id__is_active=True
        ).distinct().annotate(
            avg_price=Avg("stock__price")
        ).order_by("?").select_related("category__parent")

        return queryset[:limit]


class DailyOffer(models.Model):
    """Модель: предложение дня"""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="daily_offer",
        verbose_name=_("product"),
        help_text=_("daily\'s offer product"),
    )
    select_date = models.DateField(default=date.today)

    text = models.TextField(
        verbose_name=_("promo text"),
        help_text=_("daily offer promo content"),
        max_length=1500,
        default=""
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("daily offer")
        verbose_name_plural = _("daily offers")

    def __str__(self) -> str:
        return (
            f'Daily offer: product: {getattr(self.product, "title")} '
            f'on: {self.select_date}'
        )

    @classmethod
    def get_daily_offer(cls) -> Optional[DailyOffer]:
        """
        Метод для получения предложения дня

        :return: Товар дня
        :rtype: DailyOffer
        """

        queryset: QuerySet[DailyOffer] = DailyOffer.objects.filter(
            select_date=date.today()
        ).select_related(
            "product__category"
        )

        if queryset.exists():
            daily_offer: DailyOffer = queryset.latest("select_date")
            return daily_offer
        return None


class Stock(models.Model):
    """Модель: цена"""

    shop = models.ForeignKey(
        "shop.Shop",
        on_delete=models.CASCADE,
        verbose_name=_("shop id"),
        related_name="stock",
        help_text=_("stock\'s shop"),
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name=_("product id"),
        related_name="stock",
        help_text=_("stock\'s product"),
    )
    price = models.DecimalField(max_digits=9, decimal_places=2)
    count = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = _("stock")
        verbose_name_plural = _("stocks")

    def __str__(self):
        return f'Stock: product: {getattr(self.product, "title")} ' \
               f'shop: {getattr(self.shop, "name", None)}'

    @property
    def pk(self) -> int:
        return getattr(self, "id")

    @staticmethod
    def get_products_in_stock_by_shop(shop: Shop) -> QuerySet[Stock]:
        product_in_stock = Stock.objects.filter(shop=shop)
        return product_in_stock

    @classmethod
    def get_products_in_stock(cls, product: Product) -> QuerySet[Stock]:
        product_in_stock = Stock.objects.filter(product=product)
        return product_in_stock


class ProductReview(models.Model):
    """Модель: Отзыв о продукте"""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name=_("user product view product"),
        related_name="user_product_view",
        help_text=_("preview\'s product"),
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        verbose_name=_("user product view user"),
        related_name="user_product_view",
        help_text=_("preview\'s user"),
    )
    date = models.DateField(auto_now_add=True)

    text = models.TextField(
        verbose_name=_("review content"),
        help_text=_("review content"),
        max_length=1500,
        default=""
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name=_("rating"),
        help_text=_("product rating"),
        blank=True,
        null=True
        )

    objects = models.Manager()

    class Meta:
        verbose_name = _("user\'s review")
        verbose_name_plural = _("user\'s review")

    def __str__(self) -> str:
        return (
            f'{self.date}: user: {self.user}, '
            f'product: {getattr(self.product, "title")}'
        )

    @classmethod
    def get_comments(cls, product: Product) -> QuerySet[ProductReview]:
        return ProductReview.objects.filter(product=product)


class ProductImage(models.Model):
    """Модель: Изображения продукта """

    product = models.ForeignKey(
        Product,
        related_name="product",
        verbose_name=_("product of image"),
        help_text=_("product image"),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("product image"),
        upload_to=product_image_path,
        blank=True,
    )
    objects = models.Manager()

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")

    @classmethod
    def get_product_pics(cls, product: Product) -> List[ProductImage]:
        product_images = ProductImage.objects.filter(product=product).all()
        images_list = list(product_images)
        default_pic = ProductImage(
            product=product,
            image=product.image,
        )
        while len(images_list) < 1:
            images_list.append(default_pic)

        return images_list