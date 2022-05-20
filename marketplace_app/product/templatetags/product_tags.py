from django import template

from product.models import Product

register = template.Library()


@register.simple_tag
def price_format(price: int) -> str:
    """
    Преобразует цену из числа с плавающей точкой в строку

    Пример: int(633,33333333) -> str(633.33)
    """
    return '{:.2f}'.format(price)


@register.simple_tag(name='get_image')
def get_image(category):
    product = Product.objects.filter(category=category).first()
    return product.image
