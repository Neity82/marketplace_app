from typing import Dict

from info.models.seoitem import SEOItem
from product.models import Product
from shop.models import Shop


def addition_info_for_shop_pages(pk: int) -> Dict[str, str]:
    """
    Формирование дополнительных полей для имени и описания страницы магазина
    """
    return {
        'meta_title': Shop.objects.get(pk=pk).name,
        'meta_description': Shop.objects.get(pk=pk).description,
    }


def addition_info_for_product_pages(pk: int) -> Dict[str, str]:
    """
    Формирование дополнительных полей для имени и описания страницы товара
    """
    return {
        'meta_title': Product.objects.get(pk=pk).title,
        'meta_description': Product.objects.get(pk=pk).short_description,
    }


def get_addition_info(request_info) -> Dict[str, str]:
    """
    Определение дополнительных полей для формирования имени и описания страниц
    """
    addition_info_map = {
        'product': {
            'detail': addition_info_for_product_pages,
        },
        'shop': {
            'detail': addition_info_for_shop_pages,
        },
    }

    app_name = request_info.app_names[0]
    url_name = request_info.url_name

    addition_info = {
        'meta_title': '',
        'meta_description': '',
    }
    if 'pk' in request_info.kwargs:
        pk = request_info.kwargs['pk']
        addition_info = addition_info_map[app_name][url_name](pk)
    return addition_info


def seo_data(request):
    """
    Формируем имя и описание для препроцессора страницы
    """
    path_name = request.resolver_match.view_name
    request_info = request.resolver_match
    addition_info = get_addition_info(request_info)
    try:
        seo_item = SEOItem.objects.get(path_name=path_name)
        seo_item.meta_title += addition_info['meta_title']
        seo_item.meta_description += addition_info['meta_description']
        return {
            'seo': seo_item,
        }
    except Exception as e:
        return {}
