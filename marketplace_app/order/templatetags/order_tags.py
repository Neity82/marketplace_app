from typing import Dict, Optional

from django import template

from order.models import OrderEntity

register = template.Library()


@register.simple_tag(name='sum_order')
def get_sum_order(order) -> Dict[str, Optional[int]]:
    """
    Функция принимает заказ,
    возвращает общую сумму заказа без скидок
    и с учетом сидок на товары в заказе
    """

    sum_order = 0
    sum_order_with_discount = 0
    product_list = OrderEntity.objects.filter(order_id=order)
    for product in product_list:
        sum_order += product.price * product.count
        if product.price_with_discount is not None:
            sum_order_with_discount += product.price_with_discount * product.count
        else:
            sum_order_with_discount += product.price * product.count

    return {
        'sum_order': sum_order,
        'sum_order_with_discount': sum_order_with_discount
    }
