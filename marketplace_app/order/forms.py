from functools import cached_property

from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext as _

from order import models as order_models
from order.utils import db_table_exists
from user import models as user_models
from user.forms import CustomUserAddForm


class UserInfoFormAnonymous(CustomUserAddForm):
    full_name = forms.CharField()

    class Meta:
        model = user_models.CustomUser
        fields = [
            "full_name",
            "phone",
            "email",
            "password1",
            "password2",
        ]


def validate_char_fields(value):
    """Валидация текстовый полей"""
    if not any(char.isalpha() for char in value):
        raise ValidationError(
            _("%(value)s is incorrect"),
            params={"value": value},
        )


class UserInfoForm(forms.Form):
    """Форма информации о пользователе при оформлении заказа"""
    full_name = forms.CharField(
        validators=[
            validate_char_fields,
        ],
        required=False,
    )
    phone = forms.CharField(
        validators=[
            user_models.CustomUser.phone_regex,
        ],
        required=False,
    )
    email = forms.EmailField(
        validators=[
            validate_email,
        ],
        required=False,
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False,
    )


class DeliveryTypeChoices:
    """Варианты типа доставки при оформлении заказа"""
    # TODO костыль для миграций, джанго очень не любит подобные обращения в таблицу из модулей
    @db_table_exists('order_deliverytype')
    def get_choices(self) -> list:
        delivery_types = order_models.DeliveryType.objects.all()
        return [
            (
                str(delivery.id),
                delivery.name,
            )
            for delivery in delivery_types
        ]

    @cached_property
    def choices(self):
        return self.get_choices()


class DeliveryForm(forms.Form):
    """Форма доставки при оформлении заказа"""

    delivery_type = forms.ChoiceField(choices=DeliveryTypeChoices().choices)
    city = forms.CharField(
        validators=[
            validate_char_fields,
        ],
        required=False,
    )
    address = forms.CharField(
        validators=[
            validate_char_fields,
        ],
        required=False,
    )


class PaymentForm(forms.Form):
    """Форма платежа при оформлении заказа"""

    payment_types = order_models.Order.PaymentType.choices
    payment_type = forms.ChoiceField(choices=payment_types)
