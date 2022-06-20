from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from product.utils import undelete_admin
from user.forms import CustomUserChangeForm, CustomUserAddForm
from user.models import CustomUser, UserProductView, Compare, CompareEntity


class CompareEntityInline(admin.StackedInline):
    model = CompareEntity
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Представление модели пользователь в интерфейсе администратора"""
    change_form_template = "admin/undelete_change_form.html"

    form = CustomUserChangeForm
    add_form = CustomUserAddForm
    save_on_top = True

    list_display = ['id', 'email', 'last_name', 'first_name', 'middle_name', 'phone']
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

    def response_change(self, request, obj):
        undelete_admin(self, request, obj)
        return super(CustomUserAdmin, self).response_change(request, obj)


@admin.register(UserProductView)
class UserProductViewAdmin(admin.ModelAdmin):
    """Представление модели просмотренных товаров в интерфейсе администратора"""

    list_display = ['id', 'user_id', 'product_id', 'datetime']
    list_display_links = ['id']


@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    """Представление модели товаров для сравнения в интерфейсе администратора"""

    list_display = ['id', 'user_id']
    list_display_links = ['id']
    inlines = [CompareEntityInline,]


