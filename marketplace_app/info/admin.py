from django.contrib import admin


from .models import Banner, SEOItem, Settings


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


@admin.register(SEOItem)
class SEOItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass
