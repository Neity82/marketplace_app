from typing import Dict
from django.urls import ResolverMatch
from info.models import SEOItem
from product.models import Product
from shop.models import Shop
from django.views import generic


def addition_info_for_shop_pages(pk: int) -> Dict[str, str]:
    """
    Формирование дополнительных полей для имени и описания страницы магазина
    """
    return {
        "meta_title": Shop.objects.get(pk=pk).name,
        "meta_description": Shop.objects.get(pk=pk).description,
    }


def addition_info_for_product_pages(pk: int) -> Dict[str, str]:
    """
    Формирование дополнительных полей для имени и описания страницы товара
    """
    return {
        "meta_title": Product.objects.get(pk=pk).title,
        "meta_description": Product.objects.get(pk=pk).short_description,
    }


def get_addition_info(request_info) -> Dict[str, str]:
    """
    Определение дополнительных полей для формирования имени и описания страниц
    """
    addition_info_map: dict = {
        "product": {
            "detail": addition_info_for_product_pages,
        },
        "shop": {
            "detail": addition_info_for_shop_pages,
        },
    }

    app_name: str = request_info.app_names[0]
    url_name: str = request_info.url_name

    addition_info: Dict[str, str] = {
        "meta_title": "",
        "meta_description": "",
    }
    if "pk" in request_info.kwargs and \
            app_name in addition_info_map and \
            url_name in addition_info_map[app_name]:
        pk: int = request_info.kwargs["pk"]
        addition_info = addition_info_map[app_name][url_name](pk)
    return addition_info


def seo_data(request) -> Dict[str, SEOItem]:
    """
    Формируем имя и описание для препроцессора страницы
    """
    path_name: str = request.resolver_match.view_name
    request_info: ResolverMatch = request.resolver_match
    addition_info: Dict[str, str] = get_addition_info(request_info)
    try:
        seo_item: SEOItem = SEOItem.objects.get(path_name=path_name)
        seo_item.meta_title += addition_info["meta_title"]
        seo_item.meta_description += addition_info["meta_description"]
        return {
            "seo": seo_item,
        }
    except Exception:
        return {}


class AboutView(generic.TemplateView):
    template_name: str = "info/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop"] = Shop.objects.get(id=1)
        return context
