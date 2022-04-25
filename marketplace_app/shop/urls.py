"""marketplace_app.shop URL Configuration
"""
from django.urls import path
from shop.views import shop

app_name = 'shop'

urlpatterns = [
    path('shops/', shop, name='shops_detail'),
]
