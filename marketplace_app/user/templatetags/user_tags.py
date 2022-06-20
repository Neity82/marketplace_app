from typing import Dict, Union, List

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from product.models import AttributeValue, Product, Attribute, Unit
from user.models import Compare, CompareEntity

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


@register.simple_tag(name='value_dict')
def get_value(product: Product, attr: Attribute) -> Dict[str, Union[str, Unit]]:
    """
    Формируем словарь со значением атрибута и его параметром

    :param product: Объект Продукт
    :type product: Product
    :param attr: Объект Атрибут продукта
    :type attr: Attribute
    :return: Словарь со значением атрибута и его параметром
    :rtype: Dict[str, Union[str, Unit]]
    """

    value_dict: Dict = {}
    result: AttributeValue = AttributeValue.objects.filter(product=product, attribute=attr).first()
    if result.value is None:
        value_dict['value'] = '---'
    else:
        value_dict['value'] = result.value
    value_dict['unit'] = result.unit

    return value_dict


@register.simple_tag(name='hide')
def is_hide(compare: QuerySet[CompareEntity], attr: Attribute) -> bool:
    """
    Сравниваем аналогичные атрибуты товаров, если одинаковые возвращаем True

    :param compare: Список товаров сравнения
    :type compare: QuerySet[CompareEntity]
    :param attr: Атрибут товара
    :type attr: Attribute
    :return: Булевое значение - результат сравнения
    :rtype: bool
    """

    hide: bool = False

    if compare.count() == 1:
        return hide

    products_id: List[int] = [item.product_id for item in compare]
    list_attr_values: QuerySet[AttributeValue] = AttributeValue.objects.values_list(
        'value', flat=True
    ).filter(
        product_id__in=products_id,
        attribute=attr
    )

    if len(set(list_attr_values)) == 1:
        hide = True

    return hide


@register.simple_tag(name='head_count')
def get_count(request: WSGIRequest) -> int:
    """
    Получаем количество товаров для сравнения в шапке сайта

    :param request: django wsgi реквест
    :type request: WSGIRequest
    :return: Количество товаров
    :rtype: int
    """
    compare = Compare.get_compare(request)
    result = Compare.count(compare_id=compare.id)
    return result


