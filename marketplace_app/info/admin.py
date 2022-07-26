from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect
from django.core.cache import cache
from django.urls import path, reverse
from .forms import SEOItemForm
from .models import Banner, SEOItem, Settings

from modeltranslation.admin import TranslationAdmin


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
    """Класс регистрации в админке модели Settings"""

    change_list_template = "info/settings_change_list.html"
    list_display = ("__str__", "value")

    def get_urls(self) -> list:
        urls: list = super().get_urls()
        action_urls = [
            path("clear_cache/", self.admin_site.admin_view(self.clear_cache))
        ]
        return action_urls + urls

    def clear_cache(self, request: HttpRequest) -> HttpResponseRedirect:
        """Функция для сброса кэша"""
        key: str = request.POST.get("cache", None)
        if key is not None:
            for key_string in list(cache._cache.keys()):
                _, _, cache_key = key_string.split(sep=":")
                if key in cache_key:
                    cache.delete(cache_key)
        return HttpResponseRedirect(
            reverse(
                "admin:{app_label}_{model_name}_changelist".format(
                    app_label=self.opts.app_label, model_name=self.opts.model_name
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
