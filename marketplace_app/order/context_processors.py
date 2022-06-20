from django.core.handlers.wsgi import WSGIRequest

from order.models import Cart


def cart(request: WSGIRequest) -> dict:
    return {
        "cart": Cart.get_cart(request)
    }
