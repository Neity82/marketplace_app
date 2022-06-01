"""marketplace_app.product URL Configuration
"""
from django.http import request
from django.shortcuts import render
from django.urls import path
from product.views import IndexView, ProductListView, ProductDetailView

app_name = 'product'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('catalog/', ProductListView.as_view(), name='list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
