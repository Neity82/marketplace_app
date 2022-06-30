from django.core.handlers.wsgi import WSGIRequest

from order.models import Cart
from order.mixins import cart_init_data


def cart(request: WSGIRequest) -> dict:
    return {
<<<<<<< HEAD
        "cart": Cart.get_cart(request)
=======
        'cart': Cart.get_cart(**cart_init_data(request))
>>>>>>> 1797d9f1756005ab8f257a6239f444f0c0e947d6
    }
