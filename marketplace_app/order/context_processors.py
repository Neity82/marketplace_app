from django.core.handlers.wsgi import WSGIRequest

from order.models import Cart
from order.mixins import cart_init_data


def cart(request: WSGIRequest) -> dict:
    return {
        "cart": Cart.get_cart(**cart_init_data(request))
    }
