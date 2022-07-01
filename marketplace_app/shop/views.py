from typing import Any, Dict
from django.apps import apps
from django.urls import reverse
from django.views import generic

from product.models import Stock
from .models import Shop
from .forms import FeedBackForm


Product = apps.get_model(app_label="product", model_name="Product")


class ShopListView(generic.ListView):
    """Представление списка магазинов"""
    model = Shop
    queryset = Shop.objects.all()
    context_object_name = "shops"
    paginate_by = 24


class ShopDetailView(generic.DetailView):
    """Представление объекта магазина"""
    model = Shop
    queryset = Shop.objects.all()
    context_object_name = "shop"

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        kwargs.update({"shop": self.get_object()})
        kwargs.update(
            {"products": Product.get_popular(shop=self.get_object())}
        )
        kwargs.update(
            {'stocks': Stock.get_products_in_stock_by_shop(self.get_object())},
        )

        return kwargs


class ContactsDetailView(generic.DetailView):
    """Класс рендеринта страницы контактов по запросу методом GET"""
    template_name = "shop/contacts_detail.html"
    context_object_name = "shop"

    def get_object(self, queryset=None):
        """Метод получения объекта магазина для вывода контактов"""
        return Shop.objects.get(name="megano")

    def get_context_data(self, **kwargs):
        """Метод формирования контекста страницы (дабавление формы)"""
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = FeedBackForm()
        return context


class ContactsFormView(generic.detail.SingleObjectMixin, generic.FormView):
    """Класс рендеринга страницы контактов магазина по запросу методом POST"""
    template_name = "shop/contacts_detail.html"
    context_object_name = "shop"
    form_class = FeedBackForm

    def get_object(self, queryset=None):
        """Метод получения объекта магазина для вывода контактов"""
        return Shop.objects.get(name="megano")

    def get_success_url(self) -> str:
        """Метод получения страницы редиректа при успешной обработке формы"""
        return reverse("shop:contacts_detail")

    def form_valid(self, form):
        """Метод обработки валидной формы"""
        form.send_email()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ContactsView(generic.View):
    """Общий класс для рендеринга страницы контактов с формой"""

    def get(self, request, *args, **kwargs):
        """Метод перенаправления на класс при запросе типа GET"""
        view: generic.View = ContactsDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Метод перенаправления на класс при запросе типа POST"""
        view: generic.View = ContactsFormView.as_view()
        return view(request, *args, **kwargs)
