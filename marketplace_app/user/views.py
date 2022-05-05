from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from user.forms import UserProfileForm, CustomAuthenticationForm, CustomUserCreationForm
from user.models import CustomUser
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
    template_name = 'user/account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        last_order = Order.objects.filter(user_id=self.request.user).earliest('datetime')
        context = super().get_context_data(**kwargs)
        context['page_active'] = 'account_active'
        context['last_order'] = last_order
        context['sum_last_order'] = last_order.order_entity_order.aggregate(sum=Sum('price'))
        context['last_product_view'] = UserProductView.objects.filter(
            user_id=self.request.user
        )[:3].select_related('product_id', 'product_id__category')
        return context


class UserProfile(LoginRequiredMixin, generic.UpdateView):
    """
    Представление страницы profile.html

    - форма для редактирования данных пользователя
    """

    model = CustomUser
    form_class = UserProfileForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_active'] = 'profile_active'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)

        if self.request.FILES:
            avatar = self.request.FILES['avatar']
            user.avatar = avatar

        full_name = form.cleaned_data.get('full_name').split()
        password = form.cleaned_data.get('password1')
        if full_name:
            last_name, first_name, middle_name = full_name_analysis(name=full_name)
            user.last_name = last_name
            user.first_name = first_name
            user.middle_name = middle_name

        if password:
            user.set_password(password)

        user.save()
        login(self.request, user)

        messages.success(self.request, f'Профиль успешно сохранен')

        return HttpResponseRedirect(reverse('user:user_profile', kwargs={'pk': user.pk}))


class HistoryOrders(LoginRequiredMixin, generic.ListView):
    """
    Представление страницы historyorder.html

    - список заказов пользователя
    """

    model = Order
    template_name = 'user/historyorder.html'
    context_object_name = 'orders_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_active'] = 'historyorder_active'
        return context

    def get_queryset(self):
        orders_list = Order.objects.filter(user_id=self.request.user)
        return orders_list


class HistoryViews(LoginRequiredMixin, generic.ListView):
    """
    Представление страницы historyview.html

    - список просмотренных товаров,
    ограничен 20 последними просмотрами
    """

    model = UserProductView
    template_name = 'user/historyview.html'
    context_object_name = 'views_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_active'] = 'historyview_active'
        return context

    def get_queryset(self):
        views_list = UserProductView.objects.filter(
            user_id=self.request.user
        )[:20].select_related(
            'product_id',
            'product_id__category'
        )
        return views_list


class CompareProduct(generic.ListView):
    """
        Представление страницы compare.html

        - список товаров для сравнения,
        ограничен 4 товарами
    """

    model = Compare
    template_name = 'user/compare.html'
    context_object_name = 'compare_list'


def user_views(request, *args, **kwargs):
    return render(request, 'user/historyview.html', {})


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'user/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('product:home')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('product:home')
