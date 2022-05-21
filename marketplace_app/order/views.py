from django.shortcuts import render
from django.views import generic

from order.models import Cart, Order


class CartView(generic.ListView):
    """
        Представление страницы Cart.html

        - список товаров в корзине пользователя
    """

    model = Cart
    template_name = 'order/cart.html'
    context_object_name = 'products'


class OrderDetail(generic.DetailView):
    """
        Представление страницы oneorder.html

        - детальная информация заказа
        - возможность оплатить заказ, если не оплачен
    """

    model = Order
    template_name = 'order/oneorder.html'
    context_object_name = 'order'


def order(request, *args, **kwargs):
    return render(request, 'order/order.html', {})


def payment(request, *args, **kwargs):
    return render(request, 'order/payment.html', {})


def paymentsomeone(request, *args, **kwargs):
    return render(request, 'order/paymentsomeone.html', {})
