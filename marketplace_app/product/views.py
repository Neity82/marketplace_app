from django.shortcuts import render


def index(request, *args, **kwargs):
    return render(request, 'product/index.html', {})


def compare(request, *args, **kwargs):
    return render(request, 'product/compare.html', {})


def product(request, *args, **kwargs):
    return render(request, 'product/product.html', {})


def catalog(request, *args, **kwargs):
    return render(request, 'product/catalog.html', {})
