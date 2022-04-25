"""marketplace_app.order URL Configuration
"""
from django.urls import path
from order.views import order, payment, paymentsomeone

app_name = 'order'

urlpatterns = [
    path('order/', order, name='order_detail'),
    path('payment/card/', payment, name='payment_card'),
    path('payment/someone/', paymentsomeone, name='payment_someone'),
]
