from django.contrib import admin

from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'phone')


# class StockEntityInline(admin.TabularInline):
#     model = StockEntity
#
#
# @admin.register(Stock)
# class StockAdmin(admin.ModelAdmin):
#     inlines = (StockEntityInline,)
#     ordering = ('shop',)
#     list_display = ('shop',)
