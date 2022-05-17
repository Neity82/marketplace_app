from django import template
from product.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Формируем словарь списков из категорий
    """
    parent_categories = [
        {"parent": item, "childs": []}
        for item
        in Category.objects.filter(parent_id=None)
                           .order_by("sort_index", "title")
    ]
    child_categories = [
        item
        for item
        in Category.objects.filter(parent_id__isnull=False)
                           .order_by("sort_index", "title")
    ]

    while child_categories:
        parent_id = child_categories[0].parent_id
        for idx in range(len(parent_categories)):
            if parent_categories[idx]["childs"]:
                for child in parent_categories[idx]["childs"]:
                    if child["parent"].id == parent_id:
                        child["childs"].append(
                            child_categories.pop(0)
                        )
                        break
            if parent_categories[idx]["parent"].id == parent_id:
                parent_categories[idx]["childs"].append(
                    {
                        "parent": child_categories.pop(0),
                        "childs": []
                    }
                )
                break
    return parent_categories
