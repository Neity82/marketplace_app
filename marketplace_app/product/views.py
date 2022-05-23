from django.db.models import QuerySet, Sum
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest, QueryDict
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, render
from datetime import date, timedelta

from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from info.models import Banner
from product.forms import ProductReviewForm
from product.models import DailyOffer, Product, Category, AttributeValue, ProductImage, \
    ProductReview, Stock


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
        context['limited_edition'] = Product.get_limited_edition(
            daily_offer=context['daily_offer']
        )

        return context


def product(request, *args, **kwargs):
    return render(request, 'product/product.html', {})


class ProductListView(generic.ListView):
    template_name = "product/catalog.html"
    paginate_by = 8
    context_object_name = "products"

    def get_queryset(self):
        result: QuerySet = (Product.objects.annotate(
            total_count=Sum("stock")
        ).filter(total_count__gt=0))
        query: str = (
            QueryDict(self.request.GET.urlencode()).dict().get("query", "")
        )
        if query:
            return result.filter(title__icontains=query)
        category: int = (
            int(self.request.GET.dict().get("category", ""))
            if self.request.GET.dict().get("category", "").isdigit()
            else 0
        )
        if not Category.objects.filter(id=category):
            category = 0
        if category:
            categories_list: list = [category]
            categories_list += [
                item[0]
                for item
                in Category.objects.only("id")
                    .filter(parent_id=category)
                    .values_list("id")
            ]
            result = result.filter(category__id__in=categories_list)
        result = result.order_by("sort_index", "title", "id")
        return result

    def post(self, request: HttpRequest, *args, **kwargs):
        search_query = QueryDict(request.POST.urlencode()).dict()["query"]
        return redirect(f"/catalog/?query={search_query}")

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        product_on_page = self.get_object()
        context['images'] = ProductImage.get_product_pics(product_on_page)
        context['attributes'] = AttributeValue.get_all_attributes_of_product(product_on_page)
        context['comments'] = ProductReview.get_comments(product_on_page)
        context['stocks'] = Stock.get_products_in_stock(product_on_page)
        context['price'] = Product.get_price_with_discount(product_on_page)
        return context

    def post(self, request, *args, **kwargs):
        product_item = self.get_object()
        post_data = request.POST.copy()
        post_data['product'] = product_item
        post_data['user'] = self.request.user
        form = ProductReviewForm(post_data)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(
            reverse(
                'product:detail',
                kwargs={
                    'pk': product_item.id,
                }
            )
        )
