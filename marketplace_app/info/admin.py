from django import forms
from django.contrib import admin

from .models import Banner, SEOItem, Settings
from .utils import get_urls


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """Класс решистрации в админке модели Banner
    """
    list_display = ['id', 'title', 'is_active']
    list_editable = ['is_active']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    """Класс решистрации в админке модели Settings
    """
    list_display = ('__str__', 'value')


def get_choices() -> list:
    return [(item, item) for item in get_urls()]


class SEOItemForm(forms.ModelForm):
    """Форма редактирования моледи SEO
    """
    def __init__(self, *args, **kwargs):
        super(SEOItemForm, self).__init__(*args, **kwargs)
        self.fields['path_name'].widget = forms.Select(choices=get_choices())

    class Meta:
        model = SEOItem
        fields = '__all__'


@admin.register(SEOItem)
class SeoItemAdmin(admin.ModelAdmin):
    """Класс решистрации в админке модели SEO
    """
    form = SEOItemForm
    list_display = (
        'id',
        'path_name',
        'meta_title',
    )
    fields = (
        'path_name',
        'meta_title',
        'meta_description',
    )
