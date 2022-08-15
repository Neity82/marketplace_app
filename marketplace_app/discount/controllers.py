from datetime import datetime
from decimal import Decimal
import pytz
from django.db.models import Q, QuerySet

from .models import BasketDiscount


def _get_discount_by_mechanism(
    base_cost: Decimal, mechanism: str, value: int
) -> Decimal:
    """Метод получения скидочной цены по механизму

    :param base_cost: Базовая цена без скидки
    :type base_cost: Decimal
    :param mechanism: Механизм скидки
    :type mechanism: str
    :param value: Значение скидки
    :type value: int
    :return: Цена со скидкой
    :rtype: Decimal
    """
    if mechanism == "P":
        return Decimal("%.2f" % (Decimal("%.2f" % ((100 - value) / 100)) * base_cost))
    elif mechanism == "F":
        return Decimal(f"{value}.00")
    elif mechanism == "S":
        return base_cost - value

    return Decimal("0.00")


def get_basket_discount(basket_count: int, basket_cost: Decimal) -> Decimal:
    """Получение значения цены конзины со скидкой

    :param basket_count: количество позиций в корзине
    :type basket_count: int
    :param basket_cost: базовая стоимость корзины
    :type basket_cost: Decimal
    :return: цена корзины со скидкой
    :rtype: Decimal
    """
    discounted_price: Decimal = Decimal("0.00")
    today: datetime = pytz.UTC.localize(datetime.today())
    basket_discounts: QuerySet[BasketDiscount] = BasketDiscount.objects.select_related(
        "discount_id"
    ).filter(
        Q(discount_id__discount_type="BD", discount_id__is_active=True)
        & (
            Q(discount_id__start_at__lte=today, discount_id__finish_at=None)
            | Q(discount_id__start_at__lte=today, discount_id__finish_at__gt=today)
        )
    )
    for basket_discount in basket_discounts:
        if (
            basket_discount.min_products_count <= basket_count
            and basket_count <= basket_discount.max_products_count
        ) or (
            basket_discount.min_basket_cost <= basket_cost
            and basket_cost <= basket_discount.max_basket_cost
        ):
            current_price: Decimal = _get_discount_by_mechanism(
                basket_cost,
                basket_discount.discount_id.discount_mechanism,
                basket_discount.discount_id.discount_value,
            )
            if discounted_price == 0 or current_price < discounted_price:
                discounted_price = current_price
    return discounted_price
