from typing import Any, Dict, List, Union, OrderedDict
import collections
from django import template
from django.core.cache import cache
from product.models import Category
from info.models import Settings
from info.utils import DEFAULT_CACHE_TIME

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Формируем словарь списков из категорий
    """
    # Если есть кэш данного набора, то возвращаем его
    category_list_cache = cache.get("category_list", default=None)
    if category_list_cache is not None:
        return category_list_cache

    categories: OrderedDict[
        int, Dict[str, Union[Category, List[Category]]]
    ] = collections.OrderedDict()
    for item in Category.objects.filter(parent_id=None).order_by("sort_index", "title"):
        categories[item.id] = {"object": item, "childs": []}
    child_categories: List[Category] = [
        item
        for item in Category.objects.filter(parent_id__isnull=False).order_by(
            "sort_index", "title"
        )
    ]

    while child_categories:
        child: Category = child_categories.pop(0)
        categories[child.parent_id]["childs"].append(child)

    # Формируем кэш данного набора параметров
    category_list_cache_time_setting: Settings = Settings.objects.filter(
        name="category_list_cache_time"
    ).first()
    category_list_cache_time = (
        int(category_list_cache_time_setting.value)
        if category_list_cache_time_setting
        else DEFAULT_CACHE_TIME
    )
    cache.set("category_list", categories, category_list_cache_time)
    return categories


@register.filter(name="update_page")
def update_page(get_dict: dict, page: int):
    get_dict["page"] = page
    return "&".join([f"{key}={value}" for key, value in get_dict.items()])


@register.filter(name="get_items")
def get_items(list_: list, index: str):
    start_idx_str, stop_idx_str = index.split(sep=":")
    return list_[int(start_idx_str) : int(stop_idx_str)]


@register.filter(name="dict_key")
def dict_key(dict_: dict, key: Any):
    return dict_[key]
