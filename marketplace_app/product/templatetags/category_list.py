from django import template
from product.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Формируем словарь списков из категорий
    """
    categories = Category.objects.all()
    categories_dict = {}
    for category in categories:
        # Основная категория
        if category.parent_id is None:
            if category not in categories_dict:
                categories_dict[category] = []
            continue

        # Распределение подкатегорий
        parent = Category.objects.filter(id=category.parent_id).first()
        if parent in categories_dict:
            categories_dict[parent].append(category)
        else:
            categories_dict[parent] = [category]
    return categories_dict
