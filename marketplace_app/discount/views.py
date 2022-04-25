from django.shortcuts import render


def sale(request, *args, **kwargs):
    return render(request, 'discount/sale.html', {})
