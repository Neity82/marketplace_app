"""marketplace_app.order URL Configuration
"""
from django.urls import path
from order.views import order_detail, order, payment, paymentsomeone, CartView

app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('order/detail/', order_detail, name='order_detail'),
    path('order/', order, name='order'),
    path('payment/card/', payment, name='payment_card'),
    path('payment/someone/', paymentsomeone, name='payment_someone'),
]
