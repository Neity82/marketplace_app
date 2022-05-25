from decimal import Decimal
from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.db import models, transaction
from django.db.models import Sum, F, Q
from django.utils.translation import gettext as _

from order import utils
from product.models import Stock
from user.models import CustomUser


class CartEntity(models.Model):
    """Модель элемента корзины"""
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='cart_entity',
        help_text=_('Cart stock'),
        blank=True
    )

    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='cart_entity',
        verbose_name=_('cart\'s ')
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        verbose_name = _('cart entity')
        verbose_name_plural = _('cart entities')
        ordering = ['-id']

    objects = models.Manager()

    def __str__(self) -> str:
        user = getattr(self.cart, 'user_id') if getattr(self.cart, 'user_id') else 'Unknown'
        return f'Cart entity: user {user}, stock: {self.stock}'


class Cart(models.Model):
    """Модель корзины"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='cart_user',
        help_text=_('Cart user'),
        blank=True,
        null=True
    )

    device = models.CharField(
        max_length=255,
        help_text=_('cookie device value'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ['-id']

    objects = models.Manager()

    def __str__(self) -> str:
        user = getattr(self, 'user_id') if getattr(self, 'user_id') else 'Unknown'
        return f'Cart: user: {user}, device: {self.device}'

    @property
    def count(self) -> int:
        field = 'quantity'
        aggregation_field = 'quantity__sum'
        count = CartEntity.objects.filter(cart=self).aggregate(Sum(field)).get(aggregation_field)
        return count

    @property
    def pk(self) -> int:
        return getattr(self, 'id')

    def __len__(self) -> int:
        return self.count

    def add_to_cart(self, stock_id: int) -> (bool, str):
        """
        Добавляем товар в корзину:
        создаем новый CartEntity или обновляем quantity у старого
        :param stock_id: id товара (складского остатка)
        :return: bool - успех добавления, сообщение
        """
        result = True
        message = utils.ADD_TO_CART_SUCCESS

        cart_entity = CartEntity.objects.filter(cart_id=self.pk, stock_id=stock_id).first()
        if cart_entity:
            if cart_entity.stock.count > cart_entity.quantity:
                cart_entity.quantity = F('quantity') + 1
                cart_entity.save()
        else:
            CartEntity.objects.create(cart_id=self.pk, stock_id=stock_id)

        return result, message

    def remove_from_cart(self, stock_id: int) -> (bool, str):
        """
        Удаляем элемент корзины из корзины
        :param stock_id: id товара (складского остатка)
        :return: - успех удаления, сообщение
        """
        result = False
        message = utils.REMOVE_FROM_CART_FAIL

        cart_entity = CartEntity.objects.filter(cart_id=self.pk, stock_id=stock_id).first()
        if cart_entity:
            cart_entity.delete()
            result = True
            message = utils.REMOVE_FROM_CART_SUCCESS
        return result, message

    def update_quantity(self, stock_id: int, quantity: int) -> (bool, str):
        """
        Обновляем количество у элемента корзины, если количество равно 0 - удаляем
        :param stock_id: id товара (складского остатка)
        :param quantity: новое количество
        :return: успех обновления, сообщение
        """
        result = False
        message = utils.UPDATE_CART_QUANTITY_FAIL

        stock = Stock.objects.filter(id=stock_id).first()
        cart_entity = CartEntity.objects.filter(cart_id=self.pk, stock_id=stock.pk).first()
        if cart_entity:
            if quantity:
                if stock.count >= quantity:
                    cart_entity.quantity = quantity
                    cart_entity.save(update_fields=['quantity'])
                    result = True
                    message = utils.UPDATE_CART_QUANTITY_SUCCESS % quantity
            else:
                result, message = self.remove_from_cart(stock_id=stock_id)
        return result, message

    def change_shop_by_id(self, stock_id: int, shop_id: int) -> (bool, str):
        """
        Меняем продавца у товара, если такой товар уже есть в корзине складываем их количество
        Если после сложения количество товара превышает складской остаток, отдаем "максимум" со склада
        :param stock_id: id товара (складского остатка)
        :param shop_id: id продавца (магазина)
        :return: успех операции, сообщение
        """
        result = True
        message = utils.CHANGE_SHOP_CART_FAIL

        with transaction.atomic():
            stock = Stock.objects.filter(id=stock_id).first()
            cart_entity = CartEntity.objects.filter(
                cart_id=self.pk, stock=stock
            ).first()

            if cart_entity:
                new_stock = Stock.objects.filter(product_id=stock.product.id, shop_id=shop_id).first()

                if new_stock not in Stock.objects.filter(cart_entity__cart=self):
                    if cart_entity.quantity >= new_stock.count:
                        new_quantity = new_stock.count
                        message = utils.UPDATE_CART_QUANTITY_LIMIT_MERGED % new_quantity
                    else:
                        new_quantity = cart_entity.quantity
                        message = utils.CHANGE_SHOP_CART_SUCCESS
                        result = True

                    cart_entity.stock = new_stock
                    cart_entity.quantity = new_quantity
                    cart_entity.save(update_fields=['stock', 'quantity', ])
                else:
                    new_cart_entity = CartEntity.objects.filter(
                        stock_id=new_stock.id, cart_id=self.pk
                    ).first()

                    if new_cart_entity.stock.count >= (
                            new_cart_entity.quantity + cart_entity.quantity
                    ):
                        new_cart_entity.quantity = F('quantity') + cart_entity.quantity
                        message = utils.CHANGE_SHOP_CART_SUCCESS
                        result = True
                    else:
                        new_cart_entity.quantity = (
                                F('quantity')
                                - new_cart_entity.quantity
                                + cart_entity.quantity
                        )
                        message = utils.UPDATE_CART_QUANTITY_LIMIT_MERGED % cart_entity.quantity

                    new_cart_entity.save()
                    cart_entity.delete()
        return result, message

    def _get_sums(self) -> (Decimal, Decimal):
        """
        Получаем суммы без скидок и со скидкой
        :return: tuple(сумма без скидок, сумма со скидкой)
        """
        old_sum = Decimal(0.0)
        discount_sum = Decimal(0.0)

        for cart_entity in CartEntity.objects.filter(cart=self).select_related("stock"):
            old_sum += Decimal(cart_entity.stock.price) * cart_entity.quantity
            if cart_entity.stock.product.discount:
                discount_sum += (
                        Decimal(cart_entity.stock.product.discount.get("price"))
                        * cart_entity.quantity
                )
            else:
                discount_sum += Decimal(cart_entity.stock.price) * cart_entity.quantity
        return old_sum, discount_sum

    def get_min_sum(self) -> Decimal:
        """Возвращаем минимальную сумму стоимости товаров"""
        return min(self._get_sums())

    def total_sums(self) -> dict:
        """Возвращаем суммы без скидок и со скидкой в виде словаря"""
        old_sum, discount_sum = self._get_sums()
        total = {'old_sum': old_sum, }
        if old_sum != discount_sum:
            total.update(discount_sum=discount_sum)
        return total

    @staticmethod
    def update_instance(instance: 'Cart', **kwargs) -> None:
        """Обновляем объект корзины из kwargs """
        updated = False
        for attr, value in kwargs.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                updated = True
        if updated:
            instance.save()

    @classmethod
    def _get_anonymous_cart(cls, device: str) -> 'Cart':
        """
        Получаем или создаем корзину для анонимного пользователя
        :return: объект Корзины
        """
        instance = Cart.objects.filter(device=device).first()
        if instance is None:
            instance = Cart.objects.create(device=device)
        return instance

    @classmethod
    def _get_user_cart(cls, user: CustomUser, device: str) -> 'Cart':
        """
        Получаем или создаем корзину для авторизованного пользователя
        :return: объект Корзины
        """
        instance = Cart.objects.filter(Q(user_id=user) | Q(device=device)).first()
        if instance is None:
            instance = Cart.objects.create(device=device, user_id=user)
        else:
            cls.update_instance(instance, device=device, user_id=user)
        return instance

    @classmethod
    def get_cart(cls, request: WSGIRequest) -> 'Cart':
        """
        Получаем объект корзины из реквеста пользователя, проверяя cookie
        :param request: django wsgi реквест
        :return: объект Корзины
        """
        user = getattr(request, 'user', None)
        device = request.COOKIES.get('device', None)

        assert user, 'can\'t get user from request!'
        # assert device, 'no "device", check static!'

        if user.is_anonymous:
            instance = cls._get_anonymous_cart(device=device)
        else:
            instance = cls._get_user_cart(user=user, device=device)
        return instance



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
    def get_last_order(cls, user: CustomUser) -> 'Order':
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
