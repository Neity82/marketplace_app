from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext as _

from user.models import CustomUser, View, Compare


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Представление модели пользователь в интерфейсе администратора"""

    form = UserChangeForm
    add_form = UserCreationForm
    save_on_top = True

    list_display = ['id', 'email', 'last_name', 'first_name', 'middle_name']
    list_display_links = ['id', 'email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal information'), {
            'fields': ('last_name', 'first_name', 'middle_name', 'phone', 'avatar')
        }),
        (_('Permission'), {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    """Представление модели просмотренных товаров в интерфейсе администратора"""

    list_display = ['id', 'user_id', 'product_id']
    list_display_links = ['id']


@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    """Представление модели товаров для сравнения в интерфейсе администратора"""

    list_display = ['id', 'user_id', 'product_id']
    list_display_links = ['id']


