from decimal import Decimal
from typing import List

from django.db import models, transaction
from django.db.models import Sum, F, Q, QuerySet
from django.utils.translation import gettext_lazy as _
from timestamps.models import SoftDeletes

from order import utils
from product.models import Stock
from user.models import CustomUser
from discount.controllers import get_basket_discount


class CartEntity(models.Model):
    """Модель элемента корзины"""

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="cart_entity",
        blank=True,
    )

    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        related_name="cart_entity",
        verbose_name=_("cart's "),
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        verbose_name = _("cart entity")
        verbose_name_plural = _("cart entities")
        ordering = ["-id"]

    objects = models.Manager()

    def __str__(self) -> str:
        user = (
            getattr(self.cart, "user_id")
            if getattr(self.cart, "user_id")
            else "Unknown"
        )
        return f"Cart entity: user {user}, stock: {self.stock}"


class Cart(models.Model):
    """Модель корзины"""

    user_id = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="cart_user",
        blank=True,
        null=True,
    )

    device = models.CharField(
        max_length=255,
        verbose_name=_("device"),
        help_text=_("cookie device value"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        ordering = ["-id"]

    objects = models.Manager()

    def __str__(self) -> str:
        user = getattr(self, "user_id") if getattr(self, "user_id") else "Unknown"
        return f"Cart: user: {user}, device: {self.device}"

    @property
    def count(self) -> int:
        field = "quantity"
        aggregation_field = "quantity__sum"
        count = (
            CartEntity.objects.filter(cart=self)
            .aggregate(Sum(field))
            .get(aggregation_field)
        )
        return count if count else 0

    @property
    def pk(self) -> int:
        return getattr(self, "id")

    def __len__(self) -> int:
        return self.count

    def add_to_cart(self, stock_id: int, cnt: int = 1) -> (bool, str):
        """
        Добавляем товар в корзину:
        создаем новый CartEntity или обновляем quantity у старого
        :param
        stock_id: id товара (складского остатка)
        cnt: количество добавляемого товара
        :return: bool - успех добавления, сообщение
        """
        result = True
        message = utils.ADD_TO_CART_SUCCESS

        cart_entity = CartEntity.objects.filter(
            cart_id=self.pk, stock_id=stock_id
        ).first()
        if cart_entity:
            if cart_entity.stock.count > cart_entity.quantity:
                cart_entity.quantity = F("quantity") + cnt
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

        cart_entity = CartEntity.objects.filter(
            cart_id=self.pk, stock_id=stock_id
        ).first()
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
        cart_entity = CartEntity.objects.filter(
            cart_id=self.pk, stock_id=stock.pk
        ).first()
        if cart_entity:
            if quantity:
                if stock.count >= quantity:
                    cart_entity.quantity = quantity
                    cart_entity.save(update_fields=["quantity"])
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

        def merge(stock: Stock, shop_id: int) -> (bool, str):
            new_stock = (
                Stock.objects.filter(product_id=stock.product.id, shop_id=shop_id)
                .select_related("shop")
                .first()
            )

            if stock.shop.pk != new_stock.shop.pk:

                if new_stock.id not in Stock.objects.filter(
                    cart_entity__cart_id=self.pk
                ).values_list("id", flat=True):
                    _result, _message = _merge_new_cart_stocks(cart_entity, new_stock)

                else:
                    _result, _message = _merge_existence_cart_stocks(
                        new_stock_id=new_stock.id, cart_id=self.pk
                    )
            else:
                _result = True
                _message = utils.CHANGE_SHOP_CART_SAME_SHOP
            return _result, _message

        def _merge_new_cart_stocks(
            _cart_entity: CartEntity, _new_stock: Stock
        ) -> (bool, str):
            _result = False
            if _cart_entity.quantity >= _new_stock.count:
                new_quantity = _new_stock.count
                _message = utils.UPDATE_CART_QUANTITY_LIMIT_MERGED % new_quantity
            else:
                new_quantity = _cart_entity.quantity
                _message = utils.CHANGE_SHOP_CART_SUCCESS
                _result = True

            _cart_entity.stock = _new_stock
            _cart_entity.quantity = new_quantity
            _cart_entity.save(
                update_fields=[
                    "stock",
                    "quantity",
                ]
            )
            return _result, _message

        def _merge_existence_cart_stocks(
            new_stock_id: int, cart_id: int
        ) -> (bool, str):
            _result = False
            new_cart_entity = CartEntity.objects.filter(
                stock_id=new_stock_id, cart_id=cart_id
            ).first()

            if new_cart_entity.stock.count >= (
                new_cart_entity.quantity + cart_entity.quantity
            ):
                new_cart_entity.quantity = F("quantity") + cart_entity.quantity
                _message = utils.CHANGE_SHOP_CART_SUCCESS
                _result = True
            else:
                new_cart_entity.quantity = (
                    F("quantity")
                    - new_cart_entity.quantity
                    + new_cart_entity.stock.count
                )
                _message = (
                    utils.UPDATE_CART_QUANTITY_LIMIT_MERGED % cart_entity.quantity
                )
            new_cart_entity.save()
            cart_entity.delete()
            return _result, _message

        result = False
        message = utils.CHANGE_SHOP_CART_FAIL

        with transaction.atomic():
            stock = Stock.objects.filter(id=stock_id).first()
            cart_entity = (
                CartEntity.objects.filter(cart_id=self.pk, stock=stock)
                .select_related("stock", "stock__shop")
                .first()
            )

            if cart_entity:
                result, message = merge(stock, shop_id)
        return result, message

    def _get_sums(self) -> (Decimal, Decimal):
        """
        Получаем суммы без скидок и со скидкой
        :return: tuple(сумма без скидок, сумма со скидкой)
        """
        old_sum = Decimal(0.0)
        product_discount_sum = Decimal(0.0)

        cart_objects: QuerySet[CartEntity] = CartEntity.objects.filter(
            cart=self
        ).select_related("stock")
        for cart_entity in cart_objects:
            old_sum += Decimal(cart_entity.stock.price) * cart_entity.quantity
            if cart_entity.stock.product.discount:
                product_discount_sum += (
                    Decimal(cart_entity.stock.product.discount.get("price"))
                    * cart_entity.quantity
                )
            else:
                product_discount_sum += (
                    Decimal(cart_entity.stock.price) * cart_entity.quantity
                )

        basket_discount_sum = Decimal(0.0)
        if len(cart_objects) > 0:
            basket_discount_sum = get_basket_discount(len(cart_objects), old_sum)
            if basket_discount_sum != 0:
                return old_sum, min(product_discount_sum, basket_discount_sum)
        return old_sum, product_discount_sum

    def get_min_sum(self) -> Decimal:
        """Возвращаем минимальную сумму стоимости товаров"""
        return min(self._get_sums())

    def total_sums(self) -> dict:
        """Возвращаем суммы без скидок и со скидкой в виде словаря"""
        old_sum, discount_sum = self._get_sums()
        total = {
            "old_sum": old_sum,
        }
        if old_sum != discount_sum:
            total.update(discount_sum=discount_sum)
        return total

    @staticmethod
    def update_instance(instance: "Cart", **kwargs) -> "Cart":
        """Обновляем объект корзины из kwargs"""
        updated = False
        for attr, value in kwargs.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                updated = True
        if updated:
            instance.save()
        return instance

    @classmethod
    def merge_carts(cls, user_cart: "Cart", anon_cart: "Cart", **kwargs) -> "Cart":
        """
        Соединяем корзины анонимного пользователя и авторизованного при авторизации
        """
        user_cart_stocks = Stock.objects.filter(cart_entity__cart_id=user_cart)
        if user_cart != anon_cart:
            for cart_entity in CartEntity.objects.filter(
                cart_id=anon_cart
            ).select_related("stock", "stock__shop"):
                if cart_entity.stock in user_cart_stocks:
                    user_cart_entity = CartEntity.objects.get(
                        cart_id=user_cart, stock_id=cart_entity.stock
                    )
                    user_cart_entity.quantity = (
                        user_cart_entity.quantity + cart_entity.quantity
                        if user_cart_entity.quantity + cart_entity.quantity
                        <= cart_entity.stock.count
                        else cart_entity.stock.count
                    )
                    user_cart_entity.save(update_fields=["quantity"])
                else:
                    cart_entity.cart = user_cart
                    cart_entity.save(update_fields=["cart"])
            user_cart = cls.update_instance(user_cart, **kwargs)
            anon_cart.delete()
        return user_cart

    @classmethod
    def _get_anonymous_cart(cls, device: str) -> "Cart":
        """
        Получаем или создаем корзину для анонимного пользователя
        :return: объект Корзины
        """
        instance = {}
        if device:
            instance = Cart.objects.filter(device=device).first()
            if instance is None:
                instance = Cart.objects.create(device=device)
        return instance

    @classmethod
    def _get_user_cart(cls, user: CustomUser, device: str) -> "Cart":
        """
        Получаем или создаем корзину для авторизованного пользователя
        :return: объект Корзины
        """
        instance = Cart.objects.filter(user_id=user).first()
        if instance is None:
            instance = Cart.objects.create(device=device, user_id=user)
        else:
            anon_carts = Cart.objects.filter(device=device).order_by("-user_id")
            if len(anon_carts) > 1:
                cls.merge_carts(
                    instance, anon_carts.first(), device=device, user_id=user
                )
            else:
                cls.update_instance(instance, device=device, user_id=user)
        return instance

    @classmethod
    def get_cart(cls, user: CustomUser, device: str) -> "Cart":
        """
        Получаем объект корзины из пользователя и id устройства
        :param user: пользователь из запроса
        :param device:
        :return: объект Корзины
        """
        if user.is_anonymous:
            instance = cls._get_anonymous_cart(device=device)
        else:
            instance = cls._get_user_cart(user=user, device=device)
        return instance

    def get_shops(self) -> set:
        """Получение множества магазинов (продавцов) у корзины"""
        shops = set()
        cart_entity_qs = CartEntity.objects.filter(cart_id=self.pk).select_related(
            "stock", "stock__shop"
        )
        for cart_entity in cart_entity_qs:
            shops.add(cart_entity.stock.shop)
        return shops


class DeliveryType(models.Model):
    """
    name - название типа доставки
    special_price - специальная цена, если сумма корзины больше cart_sum
    price - обычная цена
    cart_sum - фиксированная "стоимость" корзины для управления ценой доставки
    """

    name = models.CharField(
        max_length=50,
        verbose_name=_("name"),
    )
    special_price = models.PositiveIntegerField(
        default=0,
        verbose_name=_("special price"),
    )

    price = models.PositiveIntegerField(
        default=200,
        verbose_name=_("price"),
    )

    cart_sum = models.PositiveIntegerField(
        default=2000,
        verbose_name=_("cart price"),
    )

    class Meta:
        verbose_name = _("delivery type")
        verbose_name_plural = _("delivery types")

    def __str__(self) -> str:
        return f"{self.name}"

    objects = models.Manager()


class Delivery(models.Model):
    """Модель доставки"""

    base_delivery_id = 1
    express_delivery_id = 2

    delivery_type = models.ForeignKey(
        DeliveryType,
        on_delete=models.CASCADE,
        verbose_name=_("delivery type"),
        related_name="delivery_delivery_type",
        null=True,
    )
    city = models.CharField(max_length=50, default="")
    address = models.TextField(default="")
    price = models.DecimalField(decimal_places=2, max_digits=9, default=200)

    class Meta:
        verbose_name = _("delivery item")
        verbose_name_plural = _("delivery items")

    objects = models.Manager()

    def __str__(self):
        return f"{self.city}, {self.address}: {self.delivery_type}"

    @classmethod
    def get_delivery_data(cls, cart: Cart, delivery_type_pk: int) -> dict:
        """
        Получение данных о доставке для корзины:
            - стоимость доставки
            - название типа доставки
        """
        delivery_type_obj = DeliveryType.objects.filter(id=delivery_type_pk).first()
        return {
            "delivery_sum": cls.get_delivery_sum(cart, delivery_type_obj),
            "delivery_name": delivery_type_obj.name,
        }

    @classmethod
    def get_delivery_sum(cls, cart: Cart, delivery_type_obj: DeliveryType) -> Decimal:
        """Получение стоимости доставки для корзины"""
        cart_sum = cart.get_min_sum()
        base_delivery = DeliveryType.objects.filter(id=cls.base_delivery_id).first()
        delivery_sum = base_delivery.price

        if len(cart.get_shops()) == 1 and cart_sum > base_delivery.cart_sum:
            delivery_sum = base_delivery.special_price
        delivery_sum += delivery_type_obj.special_price

        return Decimal(delivery_sum)


class Order(SoftDeletes):
    """Модель заказа"""

    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="order_info",
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("order date"),
    )
    delivery_id = models.ForeignKey(
        Delivery,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("delivery"),
        related_name="order_delivery",
    )

    class PaymentType(models.TextChoices):
        CARD = "card", _("Card")
        SOME_ACCOUNTS = "account", _("Some accounts")

    payment_type = models.CharField(
        max_length=50,
        choices=PaymentType.choices,
        verbose_name=_("payment type"),
        default=PaymentType.CARD,
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("comment"),
    )

    class State(models.TextChoices):
        PAID = "paid", _("Paid")
        NOT_PAID = "not paid", _("Not paid")
        DELIVERY = "delivered", _("Delivered")
        RECEIVED = "received", _("Received")

    state = models.CharField(
        max_length=50,
        choices=State.choices,
        default=State.NOT_PAID,
        verbose_name=_("state"),
    )

    class Error(models.TextChoices):
        ERROR_1 = "error1", _(
            "Payment has not been completed, because you are suspected of intolerance"
        )
        ERROR_2 = "error2", _("There are not enough funds in your account")
        ERROR_3 = "error3", _("Oops... Something went wrong")

    error = models.CharField(
        max_length=250,
        choices=Error.choices,
        blank=True,
        verbose_name=_("error"),
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ["-id"]

    objects = models.Manager()

    def __str__(self) -> str:
        return f"Order №{self.pk}"

    @property
    def get_order_entity(self) -> List["OrderEntity"]:
        """Метод получения товаров в заказе

        :return: Товары в заказе
        :rtype: List["OrderEntity"]
        """

        result: List[OrderEntity] = OrderEntity.objects.filter(
            order_id=self
        ).select_related("stock_id", "stock_id__product")
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
        ).annotate(sum=F("price") * F("count"))
        for sum_entity in order_entity:
            sum_order += getattr(sum_entity, "sum", Decimal(0.0))
        sum_order += getattr(self.delivery_id, "price", Decimal(0.0))
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
            discounted_sum=F("discounted_price") * F("count"),
            sum=F("price") * F("count"),
        )
        for sum_entity in order_entity:
            if sum_entity.discounted_sum is None:
                discounted_sum_order += sum_entity.sum
            else:
                discounted_sum_order += sum_entity.discounted_sum
        discounted_sum_order += getattr(self.delivery_id, "price", Decimal(0.0))
        return Decimal(round(discounted_sum_order, 2))

    @classmethod
    def get_last_order(cls, user: CustomUser) -> "Order":
        """
        Метод для получения последнего оформленного заказа

        :param user: CustomUser
        :type user: CustomUser
        :return: Последний заказ
        :rtype: Order
        """

        if cls.objects.filter(user_id=user).exists():
            last_order: Order = Order.objects.filter(user_id=user).latest("datetime")
            return last_order

    @classmethod
    def create_order(
        cls, cart: Cart, delivery: Delivery, payment_type: str, user: CustomUser
    ) -> "Order":
        """Создание заказа"""
        with transaction.atomic():
            order = Order.objects.create(
                user_id=user,
                delivery_id=delivery,
                payment_type=payment_type,
            )

            for cart_entity in CartEntity.objects.filter(
                cart_id=cart.pk
            ).select_related("stock", "stock__product"):
                price = Decimal(cart_entity.stock.price)
                discounted_price = Decimal(
                    cart_entity.stock.product.discount.get("price")
                )
                OrderEntity.objects.create(
                    stock_id=cart_entity.stock,
                    order_id=order,
                    price=price,
                    discounted_price=discounted_price,
                    count=cart_entity.quantity,
                )
                cart_entity.delete()

        return order


class OrderEntity(models.Model):
    """Модель товара в заказе"""

    stock_id = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        verbose_name=_("stock"),
        related_name="order_entity_stock",
    )
    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("order"),
        related_name="order_entity_order",
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name=_("price"),
    )
    discounted_price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("discounted price"),
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("count"),
    )

    class Meta:
        verbose_name = _("order entity")
        verbose_name_plural = _("orders entity")

    objects = models.Manager()
