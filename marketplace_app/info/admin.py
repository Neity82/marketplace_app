from django.contrib import admin
from .forms import SEOItemForm
from .models import Banner, SEOItem, Settings

from modeltranslation.admin import TranslationAdmin


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    """Класс регистрации в админке модели Banner
    """
    list_display = ("id", "title", "is_active")
    list_editable = ("is_active",)

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    """Класс решистрации в админке модели Settings
    """
    list_display = ("__str__", "value")


@admin.register(SEOItem)
class SeoItemAdmin(TranslationAdmin):
    form = SEOItemForm
    list_display = (
        "id",
        "path_name",
        "meta_title",
    )
    fields = (
        "path_name",
        "meta_title",
        "meta_description",
    )

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }
