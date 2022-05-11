from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import category_icon_path, product_image_path


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
    def discount(self):
        # TODO:
        #  Необходимо реализовать получение актуального
        #   значения скидки на данный товар в процентах.
        #  Сейчас возвращает значение из шаблона.
        discount_value = 60
        return f"-{discount_value}%"

    @property
    def price(self):
        # TODO:
        #  Необходимо реализовать получение актуальной
        #   цены для продукта с учетом того, что в бд
        #   может быть несколько вхождений с разной ценой.
        #  Сейчас реализовано по методу FIFO.
        entity = self.stock.filter(count__gt=0).reverse().first()
        return entity.price

    @property
    def discounted_price(self):
        # TODO:
        #  Необходимо реализовать получение
        #   цены продукта с учетом скидки.
        #  Сейчас возвращает актуальную цену без скидки.
        return self.price

    @classmethod
    def get_popular(cls, shop=None, limit: int = 8):
        # TODO метод-заглушка для получения n популярных товаров
        queryset = Product.objects.prefetch_related(
            'stock'
        ).filter(
            stock__count__gt=0
        )

        if shop:
            queryset = queryset.filter(stock__shop=shop)

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

    class Meta:
        verbose_name = _('daily offer')
        verbose_name_plural = _('daily offers')

    def __str__(self) -> str:
        return f'Daily offer: product: {getattr(self.product, "title")} on: {self.select_date}'


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

    class Meta:
        verbose_name = _('stock')
        verbose_name_plural = _('stocks')

    def __str__(self):
        return f'Stock: product: {getattr(self.product, "title")} shop: {getattr(self.shop, "name", None)}'


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


