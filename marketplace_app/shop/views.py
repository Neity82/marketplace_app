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

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        kwargs.update({'shop': self.get_object()})
        kwargs.update({'products': Product.get_popular(shop=self.get_object())})
        return kwargs
