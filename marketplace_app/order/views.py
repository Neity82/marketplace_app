import json
import random
import typing
from collections import OrderedDict

from django import views
from django.core.handlers.wsgi import WSGIRequest
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from formtools.wizard.views import SessionWizardView

from order.mixins import CartMixin, cart_init_data
from order import forms as order_forms
from order import models as order_models
from order.utils import WRONG_REQUEST
from payments.models import Payment
from payments.forms import PaymentForm

from user import models as user_models


class CartView(CartMixin):
    """Вью Корзины"""

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса
        """
        self.cart = self.get_queryset()
        stock_id = request.POST.get("stock_id")
        quantity = request.POST.get("quantity")
        shop_id = request.POST.get("shop_id")

        message = WRONG_REQUEST
        success = False

        if stock_id:
            if quantity:
                success, message = self.cart.update_quantity(
                    stock_id=stock_id, quantity=int(quantity)
                )
            elif shop_id:
                success, message = self.cart.change_shop_by_id(
                    stock_id=stock_id, shop_id=shop_id
                )

        response_data = self.prepare_response_data(
            success=success,
            message=message.capitalize(),
            cart_count=self.cart.count,
            price=self.cart.get_min_sum(),
        )
        return HttpResponse(
            json.dumps(response_data, default=str), content_type="application/json"
        )

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """Возвращаем список элементов корзины и их стоимость"""
        self.cart = self.get_queryset()

        return render(
            request,
            template_name=self.template_name,
            context={"cart": self.cart, "total": self.get_sum()},
        )

    def get_queryset(self) -> order_models.Cart:
        """Получение объекта корзины по id"""
        # TODO добавить only
        cart_pk = self.get_cart_pk()
        return (
            self.model.objects.prefetch_related("cart_entity")
            .prefetch_related("cart_entity__stock__product")
            .prefetch_related("cart_entity__stock__shop")
            .filter(id=cart_pk)
            .first()
        )

    def get_sum(self) -> dict:
        """Получение цены продукта"""
        return self.cart.total_sums()


class AddToCartView(CartMixin):
    """Вью добавления в корзину"""

    @staticmethod
    def random_choice(values: list) -> typing.Any:
        """Рандомизируем продавца товара при добавлении в корзину согласно ТЗ"""
        return random.choice(values)

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса

        :return - json с количеством товаров в корзине и минимальной стоимостью
        """
        pk = kwargs.get("pk")
        shop = kwargs.get("shop_id")
        cnt = kwargs.get("cnt", 1)
        cart = self.get_cart()
        is_product = request.POST.get("is_product", None)
        if shop is not None:
            stock_id = shop
        elif is_product:
            stocks = self.stock_model.objects.filter(product__id=pk)
            stock_ids = stocks.values_list("id", flat=True)
            stock_id = self.random_choice(stock_ids)
        else:
            stock_id = pk

        success, message = cart.add_to_cart(stock_id=stock_id, cnt=int(cnt))
        response_data = self.prepare_response_data(
            success=success,
            message=message.capitalize(),
            cart_count=cart.count,
            price=cart.get_min_sum(),
        )
        return HttpResponse(
            json.dumps(response_data, default=str),
            content_type="application/json",
            status=200,
        )


class RemoveFromCartView(CartMixin):
    """Вью удаления из корзины"""

    def delete(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """Удаляем товар по id из kwargs"""
        stock_id = kwargs.get("pk")
        cart = self.get_cart()
        success, message = cart.remove_from_cart(stock_id=stock_id)
        response_data = self.prepare_response_data(
            success=success,
            message=message.capitalize(),
            cart_count=cart.count,
            price=cart.get_min_sum(),
        )
        return HttpResponse(
            json.dumps(response_data, default=str), content_type="application/json"
        )


class OrderDetail(generic.DetailView):
    """
        Представление страницы oneorder.html

        - детальная информация заказа
        - возможность оплатить заказ, если не оплачен
    """

    model = order_models.Order
    template_name = "order/oneorder.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if (not obj.user_id == self.request.user and not
                self.request.user.is_superuser):
            raise Http404

        return obj


class OrderView(SessionWizardView):
    """Вью оформления заказа"""

    confirm_step = "confirm"
    confirm_step_index = 3
    confirm_template = f"order/forms/{confirm_step}.html"

    done_step = "done"
    done_step_index = 4

    cart_model = order_models.Cart
    delivery_model = order_models.Delivery
    order_model = order_models.Order
    order_entity_model = order_models.OrderEntity
    user_model = user_models.CustomUser

    delivery_form_key = "delivery_form"
    payment_form_key = "payment_form"
    user_info_form_key = "user_info_form"

    cart_key = "cart"
    cart_sum_key = "cart_sum"
    delivery_sum_key = "delivery_sum"
    total_sum_key = "total_sum"

    order_forms = (
        (
            user_info_form_key,
            order_forms.UserInfoForm,
        ),
        (
            delivery_form_key,
            order_forms.DeliveryForm,
        ),
        (
            payment_form_key,
            order_forms.PaymentForm,
        ),
    )
    order_forms_templates = {
        user_info_form_key: f"order/forms/{user_info_form_key}.html",
        delivery_form_key: f"order/forms/{delivery_form_key}.html",
        payment_form_key: f"order/forms/{payment_form_key}.html",
    }

    def get_user_data(self) -> dict:
        """Получаем данные формы авторизованного пользователя"""
        user_data = {}
        user_attrs = [
            "full_name",
            "email",
            "phone",
        ]
        user = self.request.user
        for attr in user_attrs:
            user_data.update({f"{attr}": getattr(user, attr, None)})
        return OrderedDict(user_data)

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """Рендер формы по параметру или первого шага"""
        self.storage.current_step = self.steps.first
        user = getattr(request, "user", None)
        data = self.get_user_data() if user.is_authenticated else {}
        data = OrderedDict(data)
        form = self.get_form(data=data)
        return self.render(form)

    def get_template_names(self):
        """Получение шаблона для конкретного шага"""
        return [self.order_forms_templates[self.steps.current]]

    def handle_user(self, user_form: forms.BaseForm) -> forms.BaseForm:
        """Постобработка данных анонимного пользователя"""
        user = user_form.save()
        user_name_data = self.user_model.parse_user_name(
            user_form.cleaned_data.pop("full_name", dict())
        )
        for attr, value in user_name_data.items():
            setattr(user, attr, value)
        user.save(update_fields=user_name_data.keys())

        self.user_model.login_new_user(
            request=self.request,
            email=user_form.cleaned_data["email"],
            password=user_form.cleaned_data["password1"],
        )
        return user_form

    def user_info_form_handler(self, form: forms.BaseForm) -> forms.BaseForm:
        """Обработчик формы информации о пользователе"""
        if self.request.user.is_anonymous:
            user_creation_form = order_forms.UserInfoFormAnonymous(
                data=form.cleaned_data
            )
            if user_creation_form.is_valid():
                self.handle_user(user_creation_form)
            else:
                return user_creation_form
        return form

    def get_step_index(self, step: str = None) -> int:
        """Получаем индекс шага"""
        index = super().get_step_index(step)
        if index is None and step in (self.confirm_step, self.done_step):
            return self.confirm_step_index if step == self.confirm_step else self.done_step_index
        return index

    def get_step_number(self, step: str = None) -> int:
        """Получаем номер шага"""
        index = self.get_step_index(step)
        if index:
            return index + 1

    def handle_form(self, form: forms.BaseForm) -> forms.BaseForm:
        """Общий обработчик форм"""
        if isinstance(form, order_forms.UserInfoForm):
            form = self.user_info_form_handler(form)
        return form

    def store_form_data(self, form: forms.BaseForm) -> None:
        """Сохранение данных формы в сессию"""
        self.storage.set_step_data(self.steps.current, self.process_step(form))

    def handle_data(self, data: dict) -> dict:
        """Убираем префикс имени формы из ключа, для корректного рендера в шаблоне"""

        def remove_prefix(text: str, prefix: str) -> str:
            if text and prefix:
                if text.startswith(prefix):
                    return text[len(prefix) + 1:]
                return text

        goto_step = self.storage.current_step
        return {remove_prefix(k, goto_step): v for k, v in data.items()}

    def render_goto_step(self, goto_step: str, **kwargs) -> HttpResponse:
        """Отправляем форму с данными (при наличии) на рендер"""
        if goto_step == self.confirm_step:
            return self.render_confirm(**kwargs)
        self.storage.current_step = goto_step
        step_data = self.storage.get_step_data(self.steps.current)
        data = self.handle_data(step_data if step_data else {})
        form = self.get_form(
            data=data, files=self.storage.get_step_files(self.steps.current)
        )
        return self.render(form)

    def post(self, *args, **kwargs) -> HttpResponse:
        """Обработка форм для оформления заказа"""
        if not getattr(self.storage, "data", None):
            self.storage.request.session[self.prefix] = {}

        wizard_goto_step = self.request.POST.get("wizard_goto_step", None)

        if wizard_goto_step == self.done_step:
            return self.render_done({}, **kwargs)

        if self.get_step_index(self.steps.current) >= self.get_step_index(
            wizard_goto_step
        ):
            return self.render_goto_step(wizard_goto_step)
        form = self.get_form(data=self.request.POST)
        if form.is_valid():
            form = self.handle_form(form)
            if getattr(form, "errors", None):
                return self.render(form)
            self.store_form_data(form)

            if wizard_goto_step == self.confirm_step:
                return self.render_confirm(**kwargs)

            elif wizard_goto_step and wizard_goto_step in self.get_form_list():
                return self.render_goto_step(wizard_goto_step)
            else:
                return self.render_next_step(form)
        else:
            return self.render(form)

    def render_confirm(self, **kwargs):
        """Подготовка к рендеру шага "Подтверждения"""
        final_forms = OrderedDict()
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key),
            )
            if not form_obj.is_valid():
                return self.render_revalidation_failure(form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj
        return self.confirm(form_dict=final_forms, **kwargs)

    def confirm(self, form_dict, **kwargs):
        """Шаг подтверждения заказа"""
        cart = self.cart_model.get_cart(**cart_init_data(self.request))
        context = {
            form_name: form.cleaned_data for form_name, form in form_dict.items()
        }
        delivery_type_pk = int(context.get(self.delivery_form_key).get("delivery_type"))
        delivery_data = self.delivery_model.get_delivery_data(
            cart=cart, delivery_type_pk=delivery_type_pk
        )
        context.update(delivery_data)
        cart_sum = cart.get_min_sum()
        context.update(
            {
                self.cart_key: cart,
                self.cart_sum_key: cart_sum,
                self.total_sum_key: cart_sum + delivery_data.get(self.delivery_sum_key),
            }
        )
        return render(self.request, self.confirm_template, context=context, **kwargs)

    def checkout(self, context: dict, **kwargs):
        """Шаг оформления заказа"""
        delivery_data = context.get(self.delivery_form_key)
        payment_data = context.get(self.payment_form_key)
        cart = context.get(self.cart_key)

        delivery_type_pk = delivery_data.pop("delivery_type")
        delivery_type_obj = order_models.DeliveryType.objects.filter(id=delivery_type_pk).first()
        delivery_price = order_models.Delivery.get_delivery_sum(
            cart=cart, delivery_type_obj=delivery_type_obj
        )
        delivery_obj = order_models.Delivery.objects.create(
            delivery_type=delivery_type_obj, price=delivery_price, **delivery_data
        )

        order = self.order_model.create_order(
            cart=cart,
            delivery=delivery_obj,
            payment_type=payment_data.get("payment_type"),
            user=getattr(self.request, 'user'),
        )
        self.storage.reset()
        kwargs.update(pk=getattr(order, "id"))
        return HttpResponseRedirect(reverse("order:payment", kwargs=kwargs))

    def done(self, form_list: list, **kwargs) -> HttpResponse:
        """Постобработка данных и оформление заказа"""
        form_dict = kwargs.pop("form_dict")
        cart = self.cart_model.get_cart(**cart_init_data(self.request))
        context = {
            form_name: form.cleaned_data for form_name, form in form_dict.items()
        }
        context.update(
            {
                "cart": cart,
                "total": cart.total_sums(),
            }
        )
        return self.checkout(context=context, **kwargs)


class PaymentView(views.View):
    """Представление платежа"""

    CREATE_TEMPLATE = "payments/payment_form.html"
    PROCESS_TEMPLATE = "payments/progress.html"
    FORM = PaymentForm()
    REVERSE_URL = "order:payment_create"

    def get(self, request, pk):
        if Payment.objects.select_related("order").filter(order__pk=pk).exists():
            return render(request, self.PROCESS_TEMPLATE)
        order = order_models.Order.objects.only("payment_type").filter(pk=pk).first()
        payment_type = True if order.payment_type == "account" else False
        return render(
            request,
            self.CREATE_TEMPLATE,
            context={"form": self.FORM, "payment_type": payment_type},
        )

    def post(self, request, pk):
        Payment.objects.create(
            order=order_models.Order.objects.filter(pk=pk).first(),
            card=request.POST["card"],
        )
        return self.get(request, pk)
