from django.views import View

from order.models import Cart
from product.models import Stock
from user.models import CustomUser


class CartMixin(View):
    """ Миксин корзины """
    cart = None
    model = Cart

    user_model = CustomUser
    cart_model = Cart
    stock_model = Stock

    template_name = 'order/cart.html'

    def get_cart(self) -> Cart:
        """ Получение объекта корзины из реквеста пользователя"""
        return self.cart_model.get_cart(self.request)

    def get_cart_pk(self) -> int:
        """ Получение id объекта корзины """
        cart = self.get_cart()
        return getattr(cart, 'id')

    def get_stock(self, pk: int) -> Stock:
        """ Получение объекта 'Складской единицы' по id"""
        return self.stock_model.objects.filter(id=pk).first()
