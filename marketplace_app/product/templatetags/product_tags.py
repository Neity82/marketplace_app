from django import template


register = template.Library()


@register.simple_tag
def price_format(price: int) -> str:
    """
    Преобразует цену из числа с плавающей точкой в строку

    Пример: int(633,33333333) -> str(633.33)
    """
    return '{:.2f}'.format(price)
