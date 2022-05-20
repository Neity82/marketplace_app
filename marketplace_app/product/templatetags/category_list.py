from typing import Dict, List, Union, OrderedDict
import collections
from django import template
from product.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Формируем словарь списков из категорий
    """
    categories: OrderedDict[int, Dict[str, Union[Category, List[Category]]]] =\
        collections.OrderedDict()
    for item in (Category.objects.filter(parent_id=None)
                 .order_by("sort_index", "title")):
        categories[item.id] = {
            "object": item,
            "childs": []
        }
    child_categories: List[Category] = [
        item
        for item
        in Category.objects.filter(parent_id__isnull=False)
                           .order_by("sort_index", "title")
    ]

    while child_categories:
        child: Category = child_categories.pop(0)
        categories[child.parent_id]["childs"].append(child)
    return categories


@register.filter(name="update_page")
def update_page(get_dict: dict, page: int):
    get_dict["page"] = page
    return "&".join([f"{key}={value}" for key, value in get_dict.items()])


@register.filter(name='get_items')
def get(list_: list, index: str):
    start_idx_str, stop_idx_str = index.split(sep=":")
    return list_[int(start_idx_str):int(stop_idx_str)]
