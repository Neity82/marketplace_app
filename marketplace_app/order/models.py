from decimal import Decimal
from typing import List

from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext as _

from product.models import Stock
from user.models import CustomUser


class Cart(models.Model):
    """Модель корзины"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='cart_user',
        help_text=_('Cart user')
    )
    stock_id = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        verbose_name=_('stock'),
        related_name='cart_stock',
        help_text=_('Cart stock')
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('count'),
        help_text=_('Cart count')
    )

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ['-id']

    objects = models.Manager()


class Delivery(models.Model):
    """Модель вид доставки"""

    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
        help_text=_('Delivery name')
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name=_('price'),
        help_text=_('Delivery price')
    )

    class Meta:
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')

    def __str__(self) -> str:
        return f'{self.name}'

    objects = models.Manager()


class Order(models.Model):
    """Модель заказа"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='order_info',
        help_text=_('Order user')
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('order date'),
        help_text=_('Order date')
    )
    delivery_id = models.ForeignKey(
        Delivery,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('delivery'),
        related_name='order_delivery',
        help_text=_('Order delivery')
    )

    class Payment(models.TextChoices):
        CARD = 'card', _('Card')
        SOME_ACCOUNTS = 'account', _('Some accounts')

    payment = models.CharField(
        max_length=50,
        choices=Payment.choices,
        verbose_name=_('payment'),
        help_text=_('Order payment')
    )
    city = models.CharField(
        max_length=50,
        verbose_name=_('city'),
        help_text=_('Order city')
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_('address'),
        help_text=_('Order address')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('comment'),
        help_text=_('Order comment')
    )

    class State(models.TextChoices):
        PAID = 'paid', _('Paid')
        NOT_PAID = 'not paid', _('Not paid')
        DELIVERY = 'delivered', _('Delivered')
        RECEIVED = 'received', _('Received')

    state = models.CharField(
        max_length=50,
        choices=State.choices,
        default=State.NOT_PAID,
        verbose_name=_('state'),
        help_text=_('Order state')
    )

    class Error(models.TextChoices):
        ERROR_1 = 'error1', _('Payment has not been completed, because you are suspected of intolerance')
        ERROR_2 = 'error2', _('There are not enough funds in your account')
        ERROR_3 = 'error3', _('Oops... Something went wrong')

    error = models.CharField(
        max_length=250,
        choices=Error.choices,
        blank=True,
        verbose_name=_('error'),
        help_text=_('Order error')
    )

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-id']

    objects = models.Manager()

    def __str__(self) -> str:
        return f'Order №{self.pk}'

    @property
    def get_order_entity(self) -> List['OrderEntity']:
        """Метод получения товаров в заказе

        :return: Товары в заказе
        :rtype: List['OrderEntity']
        """

        result: List[OrderEntity] = OrderEntity.objects.filter(
            order_id=self
        ).select_related(
            'stock_id',
            'stock_id__product'
        )
        return result

    @property
    def sum_order(self) -> Decimal:
        """
        Получение общей суммы заказа без учета скидки

        :return: Значение суммы заказа
        :rtype: Decimal
        """

        sum_order: Decimal = Decimal(0)
        order_entity: List[OrderEntity] = OrderEntity.objects.filter(
            order_id=self.pk
        ).annotate(
            sum=F('price') * F('count')
        )
        for sum_entity in order_entity:
            sum_order += sum_entity.sum

        return Decimal(round(sum_order, 2))

    @property
    def discounted_sum_order(self) -> Decimal:
        """
        Получение общей суммы заказа с учетом скидки

        :return: Значение суммы заказа со скидкой
        :rtype: Decimal
        """

        discounted_sum_order: Decimal = Decimal(0)
        order_entity: List[OrderEntity] = OrderEntity.objects.filter(
            order_id=self.pk
        ).annotate(
            discounted_sum=F('discounted_price') * F('count'),
            sum=F('price') * F('count')
        )
        for sum_entity in order_entity:
            if sum_entity.discounted_sum is None:
                discounted_sum_order += sum_entity.sum
            else:
                discounted_sum_order += sum_entity.discounted_sum
        return Decimal(round(discounted_sum_order, 2))

    @classmethod
    def get_last_order(cls, user: CustomUser):
        """
        Метод для получения последнего оформленного заказа

        :param user: CustomUser
        :type user: CustomUser
        :return: Последний заказ
        :rtype: Order
        """

        if cls.objects.filter(user_id=user).exists():
            last_order: Order = Order.objects.filter(user_id=user).latest('datetime')
            return last_order


class OrderEntity(models.Model):
    """Модель товара в заказе"""

    stock_id = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        verbose_name=_('stock'),
        related_name='order_entity_stock',
        help_text=_('OrderEntity stock')
    )
    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('order'),
        related_name='order_entity_order',
        help_text=_('OrderEntity order')
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name=_('price'),
        help_text=_('OrderEntity price')
    )
    discounted_price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('discounted price'),
        help_text=_('OrderEntity discounted price')
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('count'),
        help_text=_('OrderEntity count')
    )

    class Meta:
        verbose_name = _('order entity')
        verbose_name_plural = _('orders entity')

    objects = models.Manager()
