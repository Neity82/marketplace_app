from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext as _

from user.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """Форма для создания нового пользователя."""

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Форма, используемая в интерфейсе администратора
    для изменения информации о пользователе и его списка прав.
    """

    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_("Raw passwords are not saved, so there is no way to see this user's password, "
                    "but you can change the password using <a href='{}'>this form</a>."),
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

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
