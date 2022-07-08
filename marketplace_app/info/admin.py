from django.contrib import admin
from django.core.cache.utils import make_template_fragment_key
from django.http import HttpRequest, HttpResponseRedirect
from django.core.cache import cache
from django.urls import path, reverse
from .forms import SEOItemForm
from .models import Banner, SEOItem, Settings

from modeltranslation.admin import TranslationAdmin

CACHES_DICT = {
    "category": "categories_list",
    "product": "product_list",
    "top_product": "top_product_list",
    "banner": "banner_list",
    "product_detail": "product_detail_cache",
}


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    """Класс регистрации в админке модели Banner"""
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
    """Класс регистрации в админке модели Settings
    """
    change_list_template = "info/settings_change_list.html"
    list_display = ("__str__", "value")

    def get_urls(self) -> list:
        urls: list = super().get_urls()
        action_urls = [
            path("clear_cache/", self.admin_site.admin_view(self.clear_cache))
        ]
        return action_urls + urls

    def clear_cache(self, request: HttpRequest) -> HttpResponseRedirect:
        """Функция для сброса кэша
        """
        key: str = ""
        for cache_name_html, cache_name in CACHES_DICT.items():
            if cache_name_html in request.POST:
                key = make_template_fragment_key(cache_name)
                break
        if key:
            cache.delete(key)
        return HttpResponseRedirect(
            reverse(
                "admin:{app_label}_{model_name}_changelist".format(
                    app_label=self.opts.app_label,
                    model_name=self.opts.model_name
                )
            )
        )


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
