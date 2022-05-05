from django.db import models
from django.utils.translation import gettext as _

from product.models import Stock
from user.models import CustomUser


class Cart(models.Model):
    """Модель корзины"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('cart'),
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

    def __str__(self) -> str:
        return f'Order №{self.pk}'


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
    price_with_discount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('price with discount'),
        help_text=_('OrderEntity price with discount')
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('count'),
        help_text=_('OrderEntity count')
    )

    class Meta:
        verbose_name = _('order entity')
        verbose_name_plural = _('orders entity')


