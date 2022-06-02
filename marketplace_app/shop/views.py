from django.apps import apps
from django.views import generic


from .models import Shop


Product = apps.get_model(app_label='product', model_name='Product')


class ShopListView(generic.ListView):
    """Представление списка магазинов"""
    model = Shop
    queryset = Shop.objects.all()
    context_object_name = 'shops'
    paginate_by = 24


class ShopDetailView(generic.DetailView):
    """Представление объекта магазина"""
    model = Shop
    queryset = Shop.objects.all()
    context_object_name = 'shop'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        kwargs.update({'shop': self.get_object()})
        kwargs.update(
            {'products': Product.get_popular(shop=self.get_object())}
        )
        return kwargs


class ContactsView(generic.detail.SingleObjectMixin, generic.TemplateView):
    """Представление страницы контактов"""
    template_name = "shop/contacts_detail.html"
    context_object_name = 'shop'

    def get_object(self, queryset=None):
        return Shop.objects.get(name='megano')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
