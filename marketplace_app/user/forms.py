from bootstrap_modal_forms.mixins import CreateUpdateAjaxMixin, PopRequestMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _

from user.models import CustomUser

MESSAGES = {
    "clean_phone": _("User with this phone already exists."),
    "clean_password1": _("Required to fill in"),  # not password2
    "clean_password2": _("Passwords don't match"),  # password1 != password2

}


class CustomUserAddForm(UserCreationForm):
    """Форма для создания нового пользователя."""

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    """
    Форма, используемая в интерфейсе администратора
    для изменения информации о пользователе и его списка прав.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs["instance"]
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related("content_type")

    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and CustomUser.objects.filter(phone=phone) and self.user.phone != phone:
            raise forms.ValidationError(MESSAGES["clean_phone"])
        return phone

    def clean_password(self):
        return self.initial["password"]


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя,
    а так же для смены пароля
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs["instance"]
        super(UserProfileForm, self).__init__(*args, **kwargs)

    avatar = forms.CharField(label=_("avatar").capitalize(),
                             widget=forms.FileInput(attrs={"class": "form-input"}),
                             required=False)
    full_name = forms.CharField(label=_("full name").capitalize(),
                                widget=forms.TextInput(attrs={"class": "form-input"}),
                                required=False)
    phone = forms.CharField(label=_("phone").capitalize(),
                            widget=forms.TextInput(attrs={"class": "form-input phone"}),
                            required=False)
    email = forms.CharField(label=_("e-mail").capitalize(),
                            widget=forms.TextInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label=_("password").capitalize(),
                                widget=forms.TextInput(attrs={
                                    "class": "form-input",
                                    "placeholder": _("Here you can change the password")
                                }),
                                required=False)
    password2 = forms.CharField(label=_("confirm password").capitalize(),
                                widget=forms.TextInput(attrs={
                                    "class": "form-input",
                                    "placeholder": _("Enter the password again")
                                }),
                                required=False)

    class Meta:
        model = CustomUser
        fields = ("avatar", "full_name", "email", "phone", "password1", "password2")

    def clean_phone(self):
        phone_clean = self.cleaned_data.get("phone")

        if not phone_clean:
            return phone_clean

        phone = "".join([i for i in phone_clean if i.isdigit()])[1:]
        if phone and CustomUser.objects.filter(phone=phone) and self.user.phone != phone:
            raise forms.ValidationError(MESSAGES["clean_phone"])
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and not password2:
            raise forms.ValidationError(MESSAGES["clean_password1"])
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(MESSAGES["clean_password2"])
        return password2


class CustomAuthenticationForm(AuthenticationForm):
    """Форма для аутентификации пользователей"""

    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    """Форма для регистрации пользователей"""

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "phone",
            "first_name",
            "middle_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and CustomUser.objects.filter(phone=phone):
            raise forms.ValidationError(MESSAGES["clean_phone"])
        return phone
