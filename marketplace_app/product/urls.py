"""marketplace_app.product URL Configuration
"""
from django.http import request
from django.shortcuts import render
from django.urls import path
from product.views import index

app_name = 'product'

urlpatterns = [
    path('', index, name='blog_list'),
]
