from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from user.forms import UserProfileForm
from user.models import CustomUser
from user.utils import full_name_analysis


class UserAccount(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'user/account.html'
    context_object_name = 'user'


class UserProfile(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'user/profile.html'

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


def user_orders(request, *args, **kwargs):
    return render(request, 'user/historyorder.html', {})


def user_views(request, *args, **kwargs):
    return render(request, 'user/historyview.html', {})
