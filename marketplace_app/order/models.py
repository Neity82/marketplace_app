from django.db import models
from django.utils.translation import gettext as _

from user.models import CustomUser


PAYMENT_CHOICES = [
    ('card', _('Card')),
    ('some accounts', _('Some accounts')),
]

STATE_CHOICES = [
    ('paid', _('Paid')),
    ('not paid', _('Not paid')),
    ('delivered', _('Delivered')),
    ('received', _('Received')),
]

ERROR_CHOICES = [
    ('error1', _('Payment has not been completed, because you are suspected of intolerance')),
    ('error2', _('There are not enough funds in your account')),
    ('error3', _('Oops... Something went wrong'))
]


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
    """Модель заказ"""

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
        help_text=_('Order delivery')
    )
    payment = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
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
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        verbose_name=_('state'),
        help_text=_('Order state')
    )
    error = models.CharField(
        max_length=250,
        choices=ERROR_CHOICES,
        blank=True,
        verbose_name=_('error'),
        help_text=_('Order error')
    )

    class Meta:
        verbose_name = _('info about order')
        verbose_name_plural = _('info about orders')
        ordering = ['-id']

    def __str__(self) -> str:
        return f'{self.pk}'




