from datetime import date, timedelta

from django.shortcuts import render
from django.views import generic

from info.models import Banner
from product.models import DailyOffer, Product, Category


class IndexView(generic.TemplateView):
    """
        Представление страницы index.html

        - блок с баннерами;
        - три избранные категории товаров;
        - блок «Предложение дня»;
        - каталог топ-товаров;
        - слайдер с горячими предложениями;
        - слайдер с ограниченным тиражом
        """

    template_name = 'product/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner_list'] = Banner.get_banners()
        context['popular_category'] = Category.get_popular()
        context['popular_products'] = Product.get_popular()

        day = date.today() + timedelta(days=1)
        date_str = f'{day.day}.{day.month}.{day.year} 00:00'
        context['finish_day'] = date_str

        context['daily_offer'] = DailyOffer.get_daily_offer()
        context['hot_offers'] = Product.get_product_with_discount()
        context['limited_edition'] = Product.get_limited_edition(daily_offer=context['daily_offer'])

        return context


def product(request, *args, **kwargs):
    return render(request, 'product/product.html', {})


class ProductListView(generic.ListView):
    template_name: str = "product/catalog.html"

    def get_queryset(self):
        return Product.objects.all()
