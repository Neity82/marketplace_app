from django.shortcuts import render


def order(request, *args, **kwargs):
    return render(request, 'order/order.html', {})


def payment(request, *args, **kwargs):
    return render(request, 'order/payment.html', {})


def paymentsomeone(request, *args, **kwargs):
    return render(request, 'order/paymentsomeone.html', {})
