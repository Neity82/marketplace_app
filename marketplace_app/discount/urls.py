"""marketplace_app.discount URL Configuration
"""
from django.urls import path
from discount.views import sale

app_name = 'discount'

urlpatterns = [
    path('sales/', sale, name='sales_list'),
]
