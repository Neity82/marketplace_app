from django.contrib import admin

from .models import Discount, ProductDiscount, SetDiscount, BasketDiscount


class ProductDiscountInline(admin.TabularInline):
    model = ProductDiscount
    extra = 1


class SetDiscountInline(admin.TabularInline):
    model = SetDiscount
    extra = 1


class BasketDiscountInline(admin.TabularInline):
    model = BasketDiscount
    extra = 1


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    class Media:
        js = (
            "https://code.jquery.com/jquery-3.5.1.min.js",
            "js/change_inlines.js",
        )

    inlines = [ProductDiscountInline, SetDiscountInline, BasketDiscountInline]
