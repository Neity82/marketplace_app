import json
import random
import typing

from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from order.mixins import CartMixin
from order.models import Order


class CartView(CartMixin):
    """Вью Корзины"""

    def post(self, request, *args, **kwargs):
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса
        """
        self.cart = self.get_queryset()
        stock_id = request.POST.get('stock_id')
        quantity = request.POST.get('quantity')
        shop_id = request.POST.get('shop_id')
        if stock_id:  # TODO else: Http404 ?
            if quantity:
                self.cart.update_quantity(stock_id=stock_id, quantity=int(quantity))
            elif shop_id:
                self.cart.change_shop_by_id(stock_id=stock_id, shop_id=shop_id)

        response_data = {
            'cart_count': self.cart.count,
            'price': self.cart.get_min_sum()
        }
        return HttpResponse(
            json.dumps(
                response_data, default=str
            ),
            content_type="application/json"
        )

    def get(self, request, *args, **kwargs):
        """Возвращаем список элементов корзины и их стоимость"""
        self.cart = self.get_queryset()

        return render(
            request,
            template_name=self.template_name,
            context={'cart': self.cart, 'total': self.get_sum()}
        )

    def get_queryset(self):
        """ Получение объекта корзины по id """
        # TODO добавить only
        cart_pk = self.get_cart_pk()
        return self.model.objects.prefetch_related('cart_entity').prefetch_related(
            'cart_entity__stock__product').prefetch_related('cart_entity__stock__shop').filter(id=cart_pk).first()

    def get_sum(self) -> dict:
        """ Получение цены продукта """
        return self.cart.total_sums()


class AddToCartView(CartMixin):
    """ Вью добавления в корзину """

    @staticmethod
    def random_choice(values: list) -> typing.Any:
        """ Рандомизируем продавца товара при добавлении в корзину согласно ТЗ """
        return random.choice(values)

    def post(self, request, *args, **kwargs):
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса

        :return - json с количеством товаров в корзине и минимальной стоимостью
        """
        pk = kwargs.get('pk')
        cart = self.get_cart()
        is_product = request.POST.get('is_product', None)
        if is_product:
            stock_ids = self.stock_model.objects.filter(product__id=pk).values_list('id')
            stock_id = self.random_choice(stock_ids)[0]
        else:
            stock_id = pk
        cart.add_to_cart(stock_id=stock_id)
        response_data = {
            'cart_count': cart.count,
            'price': cart.get_min_sum()
        }
        return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")


class RemoveFromCartView(CartMixin):
    """Вью удаления из корзины"""

    def delete(self, request, *args, **kwargs):
        """Удаляем товар по id из kwargs"""
        stock_id = kwargs.get('pk')
        cart = self.get_cart()
        cart.remove_from_cart(stock_id=stock_id)
        response_data = {
            'cart_count': cart.count,
            'price': min(cart.total_sums().values())
        }
        return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")


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
