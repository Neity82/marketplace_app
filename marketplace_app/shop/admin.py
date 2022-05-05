from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('display_image', 'name',  'phone')

    @staticmethod
    def display_image(obj):
        return mark_safe(f'<img src="{obj.image.url}"  height="150" />')


# class StockEntityInline(admin.TabularInline):
#     model = StockEntity
#
#
# @admin.register(Stock)
# class StockAdmin(admin.ModelAdmin):
#     inlines = (StockEntityInline,)
#     ordering = ('shop',)
#     list_display = ('shop',)
