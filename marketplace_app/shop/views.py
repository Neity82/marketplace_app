from django.apps import apps
from django.views import generic

from .models import Shop


Product = apps.get_model(app_label='product', model_name='Product')


class ShopListView(generic.ListView):
    model = Shop
    queryset = Shop.objects.all()
    context_object_name = 'shops'


class ShopDetailView(generic.DetailView):
    model = Shop
    queryset = Shop.objects.all()
    context_object_name = 'shop'

    # TODO: необходимо отфильтровать products_queryset по
    #  признаку принадлежности к конкретному магазину (pk из request) и
    #  по признаку "популярности" продукта
    products_queryset = Product.objects.all()[:8]
    extra_context = {'products': products_queryset}
