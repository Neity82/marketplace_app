from django.views import generic
from django.shortcuts import render
from .models import Product


def index(request, *args, **kwargs):
    return render(request, 'product/index.html', {})


def compare(request, *args, **kwargs):
    return render(request, 'product/compare.html', {})


def product(request, *args, **kwargs):
    return render(request, 'product/product.html', {})


class ProductListView(generic.ListView):
    template_name: str = "product/catalog.html"

    def get_queryset(self):
        return Product.objects.all()
