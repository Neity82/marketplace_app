from datetime import date, timedelta

from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from info.models import Banner
from product.models import DailyOffer, Product, Stock
from product.utils import get_random_item


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

        context['banner_list'] = Banner.objects.filter(is_active=True).order_by('?')[:3]

        product_of_day_list = DailyOffer.objects.filter(select_date=date.today())
        stock_prod_id = Stock.objects.values_list('product_id', flat=True)
        if product_of_day_list.exists():
            product_of_day = product_of_day_list.latest('select_date')
            context['product_of_day'] = product_of_day
            limited_edition = Product.objects.filter(Q(id__in=set(stock_prod_id)) &
                                                     ~Q(id=product_of_day.product_id)
                                                     ).filter(is_limited=True)
        else:
            limited_edition = Product.objects.filter(id__in=set(stock_prod_id), is_limited=True)
        context['limited_edition'] = get_random_item(limited_edition, 16)

        day = date.today() + timedelta(days=1)
        date_str = f'{day.day}.{day.month}.{day.year} 00:00'
        context['finish_day'] = date_str





        return context


def product(request, *args, **kwargs):
    return render(request, 'product/product.html', {})


def catalog(request, *args, **kwargs):
    return render(request, 'product/catalog.html', {})
