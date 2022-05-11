from typing import Dict

from django import template
from django.db.models import Avg, Max, Min

from discount.models import ProductDiscount
from product.models import Stock

register = template.Library()


@register.simple_tag(name='get_avg_price')
def get_average_price(product_view) -> Dict[str, str]:
    """
    Функция принимает объект модели UserProductView
    (просмотренный пользователем товар) и возвращает словарь со значениями
    средней цены за товар, средней цены за товар с учетом скидки и
    размер максимальной скидки
    """

    product = product_view.product_id
    avg_price_new_str = None
    max_discount_str = None

    avg_price_dict = Stock.objects.filter(product=product).aggregate(avg=Avg('price'))
    avg_price = avg_price_dict['avg']
    avg_price_str = '{:.2f}'.format(avg_price)

    discount_list = ProductDiscount.objects.filter(product_id=product,
                                                   discount_id__discount_type='PD',
                                                   discount_id__is_active=True
                                                   ).select_related('discount_id')

    if discount_list.exists():
        avg_price_minus_percent, avg_price_minus_sum, avg_price_fix = None, None, None

        max_discount_percent = discount_list.filter(
            discount_id__discount_mechanism='P'
        ).aggregate(max_discount=Max('discount_id__discount_value'))
        max_discount_sum = discount_list.filter(
            discount_id__discount_mechanism='S'
        ).aggregate(max_discount=Max('discount_id__discount_value'))
        max_discount_fix = discount_list.filter(
            discount_id__discount_mechanism='F'
        ).aggregate(min_price=Min('discount_id__discount_value'))

        if max_discount_percent['max_discount'] is not None:
            avg_price_minus_percent = float(avg_price) * (1 - max_discount_percent['max_discount'] / 100)
        if max_discount_sum['max_discount'] is not None:
            avg_price_minus_sum = float(avg_price) - max_discount_sum['max_discount']
        if max_discount_fix['min_price'] is not None:
            avg_price_fix = max_discount_fix['min_price']

        avg_price_new = min(filter(lambda i: i is not None,
                                   (avg_price_minus_percent, avg_price_minus_sum, avg_price_fix))
                            )
        if avg_price_new <= 0:
            avg_price_new = 1

        max_discount = round((1 - avg_price_new / float(avg_price)) * 100)

        max_discount_str = str(max_discount)
        avg_price_new_str = '{:.2f}'.format(avg_price_new)

    return {
        'avg_price': avg_price_str,
        'avg_price_new': avg_price_new_str,
        'max_discount': max_discount_str
    }


@register.simple_tag(name='stars')
def get_rating(rating: int) -> range:
    """
    Функция принимает рейтинг товара и возвращает range
    для отрисовки количества звезд в шаблоне
    """

    return range(rating)


@register.simple_tag(name='not_stars')
def get_rating(rating: int) -> range:
    """
    Функция принимает рейтинг товара и возвращает range
    для отрисовки неактивных звезд в шаблоне
    """

    count = 5 - rating
    return range(count)

