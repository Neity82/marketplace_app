"""marketplace_app.product URL Configuration
"""
from django.http import request
from django.shortcuts import render
from django.urls import path
from product.views import index, product, ProductListView

app_name = 'product'

urlpatterns = [
    path('', index, name='home'),
    # пока catalog, когда появятся модели отделим на products и product/pk
    path('catalog/', ProductListView.as_view(), name='list'),
    path('products/', product, name='detail'),
    path('products/<int:id>/', product, name='detail'),
]
