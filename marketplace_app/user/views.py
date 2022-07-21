import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from order.models import Order
from payments.models import Payment
from product.models import AttributeValue
from user.forms import UserProfileForm, CustomAuthenticationForm, CustomUserCreationForm
from user.mixin import ResponseDataMixin
from user.models import CustomUser, UserProductView, Compare
from user.utils import full_name_analysis

from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView


class UserAccount(LoginRequiredMixin, generic.DetailView):
    """
    Представление страницы account.html

    - информация о пользователе;
    - информация о последнем заказе;
    - последние просмотренные товары
    """

    model = CustomUser
    template_name = "user/account.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_active"] = "account_active"
        context["last_order"] = Order.get_last_order(user=self.request.user)
        context["product_view"] = UserProductView.get_product_view(user=self.request.user,
                                                                   limit=3)
        context["payment"] = Payment.objects.filter(order=context["last_order"])
        return context


class UserProfile(LoginRequiredMixin, generic.UpdateView):
    """
    Представление страницы profile.html

    - форма для редактирования данных пользователя
    """

    model = CustomUser
    form_class = UserProfileForm
    template_name = "user/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_active"] = "profile_active"
        return context

    def get_form_kwargs(self):
        kwargs = super(UserProfile, self).get_form_kwargs()
        kwargs.update({
            "initial": {
                "full_name": self.request.user.get_full_name,
            }
        })
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)

        if self.request.FILES:
            avatar = self.request.FILES["avatar"]
            if avatar.size > 2 * 1024 * 1024:
                messages.error(self.request,
                               _("Image file too large ( > 2mb )"),
                               extra_tags="error")
                return HttpResponseRedirect(reverse("user:user_profile",
                                                    kwargs={"pk": user.pk}))
            user.avatar = avatar
        else:
            avatar = self.request.user.avatar
            user.avatar = avatar

        full_name = form.cleaned_data.get("full_name")
        password = form.cleaned_data.get("password1")
        if full_name:
            user_name_data = full_name_analysis(full_name=full_name)
            user.last_name = user_name_data["last_name"]
            user.first_name = user_name_data["first_name"]
            user.middle_name = user_name_data["middle_name"]
        else:
            user.last_name = ""
            user.first_name = ""
            user.middle_name = ""

        if password:
            user.set_password(password)

        user.save()
        login(self.request, user)
        messages_text = _("Profile saved successfully")
        messages.success(self.request, messages_text, extra_tags="success")

        return HttpResponseRedirect(reverse('user:user_profile', kwargs={"pk": user.pk}))


class HistoryOrders(LoginRequiredMixin, generic.ListView):
    """
    Представление страницы historyorder.html

    - список заказов пользователя
    """

    model = Order
    template_name = "user/historyorder.html"
    context_object_name = "orders_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_active"] = "historyorder_active"
        return context

    def get_queryset(self):
        orders_list = Order.objects.filter(user_id=self.request.user)
        return orders_list


class HistoryViews(LoginRequiredMixin, ResponseDataMixin, generic.ListView):
    """
    Представление страницы historyview.html

    - список просмотренных товаров,
    ограничен 20 последними просмотрами
    """

    model = UserProductView
    template_name = "user/historyview.html"
    context_object_name = "views_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_active"] = "historyview_active"
        return context

    def get_queryset(self):
        views_list = UserProductView.get_product_view(user=self.request.user, limit=20)
        return views_list

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса
        """

        product_id = kwargs["pk"]
        success, message = UserProductView.add_object(
            user=self.request.user,
            product=product_id
        )

        response_data = self.prepare_response_data(
            success=success,
            message=message.capitalize()
        )

        return HttpResponse(
            json.dumps(response_data, default=str),
            content_type="application/json"
        )


class CompareProduct(ResponseDataMixin, generic.ListView):
    """
        Представление страницы compare.html

        - список товаров для сравнения,
        ограничен 4 товарами
    """

    model = Compare
    template_name = "user/compare.html"
    context_object_name = "compare_list"

    def get_context_data(self, **kwargs):
        compare = Compare.get_compare(self.request)

        context = super().get_context_data(**kwargs)
        context["categories"] = Compare.get_categories(compare_id=compare)
        if self.kwargs["pk"] == 0:
            context["cat_selected"] = 0
        else:
            if self.object_list.count() == 0:
                category_id = 0
            else:
                category_id = self.object_list[0].product.category_id
            context["cat_selected"] = category_id
        context["total_count"] = Compare.count(compare_id=compare)

        if self.object_list.count() > 0:
            context["attributes"] = AttributeValue.get_all_attributes_of_product(
                self.object_list[0].product_id)

        else:
            messages_text = _("Not enough data to compare")
            messages.success(self.request, messages_text)

        return context

    def get_queryset(self, **kwargs):
        compare = Compare.get_compare(self.request)
        result = Compare.get_compare_list(compare_id=compare.id)
        if self.kwargs["pk"] != 0:
            result = result.filter(product__category=self.kwargs["pk"])

        return result

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """
        Обработка POST запроса:
        от клиента получаем идентификаторы и флаги
        для последующей обработки запроса
        """

        product_id = kwargs["pk"]
        compare = Compare.get_compare(self.request)
        success, message = compare.add_to_compare(product_id=product_id)
        count = Compare.count(compare_id=compare.id)

        response_data = self.prepare_response_data(
            success=success,
            message=message.capitalize(),
            head_count=count
        )

        return HttpResponse(
            json.dumps(response_data, default=str),
            content_type="application/json"
        )

    def delete(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        """Удаляем товар по id из kwargs"""

        product_id = kwargs["pk"]
        compare = Compare.get_compare(self.request)
        success, message = compare.remove_from_compare(product_id=product_id)
        count = Compare.count(compare_id=compare.id)

        response_data = self.prepare_response_data(
            success=success,
            message=message.capitalize(),
            head_count=count
        )

        return HttpResponse(
            json.dumps(response_data, default=str),
            content_type="application/json"
        )


class CustomLoginView(BSModalLoginView):
    """
    Представление страницы login.html

    - аутентификация пользователя, представляет собой
    всплывающее окно
    """

    authentication_form = CustomAuthenticationForm
    template_name = "user/login.html"
    # success_message = _("Success: You were successfully logged in.")
    success_url = reverse_lazy("product:home")


class SignUpView(BSModalCreateView):
    """
        Представление страницы signup.html

        - регистрация пользователя, представляет собой
        всплывающее окно
    """

    form_class = CustomUserCreationForm
    template_name = "user/signup.html"
    # success_message = _("Success: Sign up succeeded. You can now Log in.")
    success_url = reverse_lazy("product:home")

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super(SignUpView, self).post(request, *args, **kwargs)


class PasswordResetViewCustom(PasswordResetView):
    success_url = reverse_lazy("user:password_reset_done")


class PasswordResetDoneViewCustom(PasswordResetDoneView):
    pass


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    success_url = reverse_lazy("user:password_reset_complete")

