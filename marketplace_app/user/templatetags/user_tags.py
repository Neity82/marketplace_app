from datetime import datetime
from typing import Dict

import pytz
from django import template
from django.db.models import Avg, Max, Min, Q

from discount.models import ProductDiscount
from product.models import Stock

register = template.Library()


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
