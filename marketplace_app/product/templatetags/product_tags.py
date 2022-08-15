from django import template
from django.db.models.fields.files import ImageFieldFile

from product.models import Product, Category

register = template.Library()


@register.simple_tag
def price_format(price: int) -> str:
    """
    Преобразует цену из числа с плавающей точкой в строку

    Пример: int(633,33333333) -> str(633.33)
    """
    return "{:.2f}".format(price)


@register.simple_tag(name="get_image")
def get_image(category: Category) -> ImageFieldFile:
    """
    Функция принимает категорию и возвращает изображение
    первого товара из этой категории

    :param category: Категория
    :type category: Category
    :return: Изображение
    :rtype: ImageFieldFile
    """
    product: Product = Product.objects.filter(category=category).first()
    return product.image
