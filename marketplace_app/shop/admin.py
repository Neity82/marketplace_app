from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .models import Shop


class TranslationAdminMedia:
    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(Shop)
class ShopAdmin(TranslationAdmin, TranslationAdminMedia):
    ordering = ("name",)
    list_display = ("display_image", "name", "phone")

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
