"""marketplace_app.product URL Configuration
"""
from django.http import request
from django.shortcuts import render
from django.urls import path
from product.views import IndexView, product, ProductListView, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    # пока catalog, когда появятся модели отделим на products и product/pk
    path('catalog/', ProductListView.as_view(), name='list'),
    path('products/', product, name='detail'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
