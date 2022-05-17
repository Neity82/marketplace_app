from datetime import date, datetime
import pytz
from decimal import Decimal
from typing import Dict, List, Union, TYPE_CHECKING
import random

from django.db import models
from django.db.models import Q, Avg, Func, Min
from django.utils.translation import gettext_lazy as _
from .utils import category_icon_path, product_image_path


if TYPE_CHECKING:
    from discount.models import Discount


class Tag(models.Model):
    """Модель: тэг"""

    title = models.CharField(
        verbose_name=_('title'),
        help_text=_('Tag title'),
        max_length=50,
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self) -> str:
        return getattr(self, 'title')


class Category(models.Model):
    """Модель: категория"""

    SEP = ' / '

    parent = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name=_('parent id'),
        related_name='child',
        help_text=_('Parent category'),
        null=True,
        blank=True,
        default=None,
    )

    title = models.CharField(
        verbose_name=_('title'),
        help_text=_('Category title'),
        max_length=50,
    )

    icon = models.ImageField(
        verbose_name=_('icon'),
        help_text=_('Category icon'),
        null=True,
        default=None,
        upload_to=category_icon_path,
    )

    sort_index = models.SmallIntegerField(
        verbose_name=_('sort index'),
        help_text=_('Sort index'),
        default=0
    )

    # TODO в качестве привязки аттрибутов к категории
    #  рассмотреть EAV:
    #   - https://pypi.org/project/eav-django/
    #   - https://github.com/mvpdev/django-eav
    #  рассмотреть JSONFiled:
    #   - https://github.com/jrief/django-entangled
    #   - https://github.com/abogushov/django-admin-json-editor

    objects = models.Manager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self) -> str:
        return self.get_category_recur()

    def get_category_recur(self) -> str:
        """Рекурсивно получаем тайтлы категорий и их родителей"""
        title = getattr(self, "title")
        parent = getattr(self, "parent")
        return (f'{parent.get_category_recur()}{self.SEP}{title}'
                if parent else title)

    @classmethod
    def get_popular(cls, limit: int = 3):
        # TODO метод-заглушка для получения n избранных категорий товаров
        queryset = Category.objects.prefetch_related(
            'product'
        ).filter(
            product__stock__count__gt=0,
        ).distinct().annotate(
            min_price=Min('product__stock__price')
        ).order_by(
            '-sort_index'
        )

        return queryset[:limit]


class Attribute(models.Model):
    """
    Модель: характеристика
    """
    title = models.CharField(
        verbose_name=_('title'),
        help_text=_('Category title'),
        max_length=50,
    )

    category = models.ForeignKey(
        'Category',
        verbose_name=_('attribute\'s category'),
        related_name='attribute',
        on_delete=models.CASCADE,
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
    value = models.CharField(max_length=255, verbose_name=_('value'))

    attribute = models.OneToOneField(
        'Attribute',
        verbose_name=_('attribute\'s value'),
        related_name='attribute_value',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("attribute value")
        verbose_name_plural = _("attribute values")

    def __str__(self) -> str:
        return getattr(self, "value")


class Product(models.Model):
    """Модель: продукт"""

    title = models.CharField(
        verbose_name=_('title'),
        help_text=_('Product title'),
        max_length=150,
    )

    image = models.ImageField(
        verbose_name=_('image'),
        help_text=_('Product image'),
        upload_to=product_image_path,
        blank=True,
    )

    short_description = models.CharField(
        verbose_name=_('short description'),
        help_text=_('Product short description'),
        max_length=150,
    )

    long_description = models.TextField(
        verbose_name=_('long description'),
        help_text=_('Product long description'),
        max_length=1500,
    )

    is_limited = models.BooleanField(
        verbose_name=_('is limited'),
        help_text=_('There is limited edition'),
        default=False,
    )

    tags = models.ManyToManyField(
        'Tag',
        related_name='products',
        related_query_name='product',
        blank=True,
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name=_('category'),
        help_text=_('Product category'),
    )

    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        help_text=_('Date the product was added'),
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
        verbose_name=_('rating'),
        help_text=_('Product rating'),
        choices=Rating.choices,
        default=Rating.ZERO,
    )

    sort_index = models.SmallIntegerField(
        verbose_name=_('sort index'),
        help_text=_('Sort index'),
        default=0
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('product')

    def __str__(self) -> str:
        category = getattr(self, "category", None)
        return (
            f"({getattr(category, 'title')}) {getattr(self, 'title')}"
            if category
            else f"{getattr(self, 'title')}"
        )

    @property
    def price(self) -> Decimal:
        entity: List[Decimal] = [
            item.price
            for item
            in self.stock.only("price")
        ]
        return round(sum(entity) / len(entity), 2)

    def _get_discounted_price(self, discount: 'Discount') -> Decimal:
        """Метод получения скидочной цены

        :param discount: Объект скидки
        :type discount: Discount
        :return: Скидочная стоимость
        :rtype: Decimal
        """
        if discount.discount_mechanism == "P":
            return round(
                (self.price * (100 - discount.discount_value) / 100), 2
            )
        elif discount.discount_mechanism == "S":
            return round((self.price - discount.discount_value), 2)
        elif discount.discount_mechanism == "F":
            return Decimal(discount.discount_value)
        return Decimal('NaN')

    @property
    def discount(self) -> Dict[str, Union[str, Decimal]]:
        """Свойство для хранения механизма скидки и скидочной стоимости

        :return: Словарь с механизмом скидки и скидочной стоимостью
        :rtype: Dict[str, Union[str, Decimal]]
        """
        discount_objects: List['Discount'] = []
        for item in self.product_discount.all():
            discount_objects.append(item.discount_id)
        for item in self.category.product_discount.all():
            discount_objects.append(item.discount_id)
        if self.category.parent_id:
            parent_category: Category = \
                Category.objects.get(id=self.category.parent_id)
            for item in parent_category.product_discount.all():
                discount_objects.append(item.discount_id)
            if parent_category.parent_id:
                root_category: Category = \
                    Category.objects.get(id=parent_category.parent_id)
                for item in root_category.product_discount.all():
                    discount_objects.append(item.discount_id)
        if not discount_objects:
            return {
                "type": None,
                "value": None,
                "price": self.price
            }
        today: datetime = pytz.UTC.localize(datetime.today())
        for idx in range(len(discount_objects)-1, -1, -1):
            if (not discount_objects[idx].is_active or
                    discount_objects[idx].start_at > today or
                    (discount_objects[idx].finish_at and
                        discount_objects[idx].finish_at < today)):
                del discount_objects[idx]
        min_discount: 'Discount' = discount_objects.pop()
        min_discounted_price: Decimal = \
            self._get_discounted_price(min_discount)
        while discount_objects:
            current_discount: 'Discount' = discount_objects.pop()
            current_discount_price: Decimal = \
                self._get_discounted_price(current_discount)
            if current_discount_price < min_discounted_price:
                min_discount = current_discount
                min_discounted_price = current_discount_price
        return {
            "type": min_discount.discount_mechanism,
            "value": min_discount.discount_value,
            "price": min_discounted_price
        }

    # @property
    # def average_price(self):
    #     """Метод для получения средней цены"""
    #     avg_price = Stock.objects.filter(
    #         product=self.pk,
    #         count__gt=0
    #     ).aggregate(avg=Avg('price'))['avg']
    #     return '{:.2f}'.format(avg_price)

    @classmethod
    def get_popular(cls, shop=None, limit: int = 8):
        # TODO метод-заглушка для получения n популярных товаров
        queryset = Product.objects.prefetch_related(
            'stock'
        ).filter(
            stock__count__gt=0
        ).distinct().annotate(
            avg_price=Avg('stock__price')
        ).order_by(
            'sort_index'
        )

        if shop:
            queryset = queryset.filter(stock__shop=shop)

        return queryset[:limit]

    @classmethod
    def get_limited_edition(cls, daily_offer=None, limit: int = 16):
        """Метод для получения списка товаров ограниченного тиража"""

        queryset = Product.objects.prefetch_related(
            'stock'
        ).filter(
            is_limited=True, stock__count__gt=0
        ).distinct().annotate(
            avg_price=Avg('stock__price')
        ).order_by('?').select_related('category__parent')

        if daily_offer:
            queryset = queryset.exclude(
                id=daily_offer.product_id)

        return queryset[:limit]

    @classmethod
    def get_product_with_discount(cls, limit: int = 9):
        """
        Метод для получения списка случайных товаров,
        на которые действует какая-нибудь акция в количестве limit
        """

        queryset = Product.objects.prefetch_related(
            'stock',
            'product_discount'
        ).filter(
            stock__count__gt=0,
            product_discount__discount_id__is_active=True
        ).distinct().annotate(
            avg_price=Avg('stock__price')
        ).order_by('?').select_related('category__parent')

        return queryset[:limit]


class DailyOffer(models.Model):
    """Модель: предложение дня"""

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='daily_offer',
        verbose_name=_('product'),
        help_text=_('Daily\'s offer product'),
    )
    select_date = models.DateField(default=date.today)

    text = models.TextField(
        verbose_name=_('promo text'),
        help_text=_('Daily offer promo content'),
        max_length=1500,
        default=''
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('daily offer')
        verbose_name_plural = _('daily offers')

    def __str__(self) -> str:
        return (
            f'Daily offer: product: {getattr(self.product, "title")}',
            f'on: {self.select_date}'
        )

    @classmethod
    def get_daily_offer(cls):
        """Метод для получения предложения дня"""

        queryset = DailyOffer.objects.filter(select_date=date.today()).annotate(
            avg_price=Avg('product__stock__price')
        ).select_related('product__category')

        if queryset.exists():
            daily_offer = queryset.latest('select_date')
            return daily_offer


class Stock(models.Model):
    """Модель: цена"""

    shop = models.ForeignKey(
        'shop.Shop',
        on_delete=models.CASCADE,
        verbose_name=_('shop id'),
        related_name='stock',
        help_text=_('Stock\'s shop'),
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_('product id'),
        related_name='stock',
        help_text=_('Stock\'s product'),
    )
    price = models.DecimalField(max_digits=9, decimal_places=2)
    count = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = _('stock')
        verbose_name_plural = _('stocks')

    def __str__(self):
        return (
            f'Stock: product: {getattr(self.product, "title")}',
            f'shop: {getattr(self.shop, "name", None)}'
        )


class ProductReview(models.Model):
    """Модель: Отзыв о продукте"""

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_('User product view product'),
        related_name='user_product_view',
        help_text=_('Preview\'s product'),
    )
    user = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=_('User product view user'),
        related_name='user_product_view',
        help_text=_('Preview\'s user'),
    )
    date = models.DateField(auto_now_add=True)

    text = models.TextField(
        verbose_name=_('review content'),
        help_text=_(''),
        max_length=1500,
        default=''
    )

    class Meta:
        verbose_name = _('user product view')
        verbose_name_plural = _('user product views')

    def __str__(self) -> str:
        return f'{self.date}: user: {self.user} product: {getattr(self.product, "title")}'
