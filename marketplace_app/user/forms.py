from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _

from user.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания нового пользователя."""

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    """
    Форма, используемая в интерфейсе администратора
    для изменения информации о пользователе и его списка прав.
    """

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = CustomUser.objects.get(email=self.cleaned_data.get('email'))
        if phone and CustomUser.objects.filter(phone=phone) and user.phone != phone:
            raise forms.ValidationError(_('A user with such a phone is already registered'))
        return phone

    def clean_password(self):
        return self.initial['password']


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя,
    а так же для смены пароля
    """

    full_name = forms.CharField(label=_('full name').capitalize(),
                                widget=forms.TextInput(attrs={'class': 'form-input'}),
                                required=False)
    phone = forms.CharField(label=_('phone').capitalize(),
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label=_('e-mail').capitalize(),
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label=_('password').capitalize(),
                                widget=forms.TextInput(attrs={
                                    'class': 'form-input',
                                    'placeholder': _('Here you can change the password')
                                }),
                                required=False)
    password2 = forms.CharField(label=_('confirm password').capitalize(),
                                widget=forms.TextInput(attrs={
                                    'class': 'form-input',
                                    'placeholder': _('Enter the password again')
                                }),
                                required=False)

    class Meta:
        model = CustomUser
        fields = ('avatar', 'full_name', 'phone', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and not password2:
            raise forms.ValidationError(_("Required to fill in"))
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2
