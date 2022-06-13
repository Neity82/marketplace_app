import json
import random
import typing

from django import views
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView

from order.mixins import CartMixin
from order.models import Order, Cart
from order.utils import WRONG_REQUEST
from payments.models import Payment
from payments.forms import PaymentForm


class CartView(CartMixin):
    """Вью Корзины"""

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса
        """
        self.cart = self.get_queryset()
        stock_id = request.POST.get('stock_id')
        quantity = request.POST.get('quantity')
        shop_id = request.POST.get('shop_id')

        message = WRONG_REQUEST
        success = False

        if stock_id:
            if quantity:
                success, message = self.cart.update_quantity(stock_id=stock_id, quantity=int(quantity))
            elif shop_id:
                success, message = self.cart.change_shop_by_id(stock_id=stock_id, shop_id=shop_id)

        response_data = self.prepare_response_data(
            success=success,
            message=message,
            cart_count=self.cart.count,
            price=self.cart.get_min_sum()
        )
        return HttpResponse(
            json.dumps(response_data, default=str),
            content_type="application/json"
        )

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """Возвращаем список элементов корзины и их стоимость"""
        self.cart = self.get_queryset()

        return render(
            request,
            template_name=self.template_name,
            context={'cart': self.cart, 'total': self.get_sum()}
        )

    def get_queryset(self) -> Cart:
        """ Получение объекта корзины по id """
        # TODO добавить only
        cart_pk = self.get_cart_pk()
        return self.model.objects.prefetch_related(
            'cart_entity'
        ).prefetch_related(
            'cart_entity__stock__product'
        ).prefetch_related(
            'cart_entity__stock__shop'
        ).filter(id=cart_pk).first()

    def get_sum(self) -> dict:
        """ Получение цены продукта """
        return self.cart.total_sums()


class AddToCartView(CartMixin):
    """ Вью добавления в корзину """

    @staticmethod
    def random_choice(values: list) -> typing.Any:
        """ Рандомизируем продавца товара при добавлении в корзину согласно ТЗ """
        return random.choice(values)

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
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
            stock_ids = self.stock_model.objects.filter(product__id=pk).values_list('id', flat=True)
            stock_id = self.random_choice(stock_ids)
        else:
            stock_id = pk

        success, message = cart.add_to_cart(stock_id=stock_id)
        response_data = self.prepare_response_data(
            success=success,
            message=message,
            cart_count=cart.count,
            price=cart.get_min_sum()
        )
        return HttpResponse(
            json.dumps(response_data, default=str),
            content_type="application/json",
            status=200
        )


class RemoveFromCartView(CartMixin):
    """Вью удаления из корзины"""

    def delete(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """Удаляем товар по id из kwargs"""
        stock_id = kwargs.get('pk')
        cart = self.get_cart()
        success, message = cart.remove_from_cart(stock_id=stock_id)
        response_data = self.prepare_response_data(
            success=success,
            message=message,
            cart_count=cart.count,
            price=cart.get_min_sum()
        )
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


class PaymentView(views.View):
    """Представление платежа"""
    CREATE_TEMPLATE = "payments/payment_form.html"
    PROCESS_TEMPLATE = "payments/progress.html"
    FORM = PaymentForm()
    REVERSE_URL = "order:payment_create"

    def get(self, request, pk):
        if Payment.objects.select_related(
                "order"
        ).filter(
            order__pk=pk
        ).exists():
            return render(request, self.PROCESS_TEMPLATE)
        order = Order.objects.only("payment_type").filter(pk=pk).first()
        payment_type = True if order.payment_type == "account" else False
        return render(request, self.CREATE_TEMPLATE, context={"form": self.FORM,
                                                              "payment_type": payment_type})

    def post(self, request, pk):
        Payment.objects.create(
            order=Order.objects.filter(pk=pk).first(),
            card=request.POST["card"],
        )
        return self.get(request, pk)
