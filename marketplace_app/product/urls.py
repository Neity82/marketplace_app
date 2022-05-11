"""marketplace_app.product URL Configuration
"""
from django.http import request
from django.shortcuts import render
from django.urls import path
from product.views import index, product, catalog

app_name = 'product'

urlpatterns = [
    path('', index, name='home'),
    # пока catalog, когда появятся модели отделим на products и product/pk
    path('catalog/', catalog, name='list'),
    path('products/', product, name='detail'),
]
