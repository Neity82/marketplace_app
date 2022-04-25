"""marketplace_app.product URL Configuration
"""
from django.http import request
from django.shortcuts import render
from django.urls import path
from product.views import index, product, compare, catalog

app_name = 'product'

urlpatterns = [
    path('', index, name='index_page'),
    path('catalog/', catalog, name='catalog_page'),
    path('product/', product, name='product_page'),
    path('compare/', compare, name='compare_page'),
]
