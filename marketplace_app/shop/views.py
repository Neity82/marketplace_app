from django.shortcuts import render


def shop(request, *args, **kwargs):
    return render(request, 'shop/shop.html', {})
