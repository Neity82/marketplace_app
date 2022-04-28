from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from product import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )
    list_display_links = (
        'id',
        'title',
    )
    search_fields = (
        'id',
        'title',
    )
    fields = ('title', )


"""
@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value',  'attribute',)
    list_display_links = ('id', 'value',)
    search_fields = ('id', 'value', 'attribute',)
    fields = ('value', 'attribute',)
"""


class AttributeValueInLine(SuperInlineModelAdmin, admin.StackedInline):
    model = models.AttributeValue
    max_num = 1


"""
@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'category', 'help_text')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'category', 'help_text',)
    fields = ('title', 'category', 'help_text')
    inlines = [AttributeValueInLine]
"""


class AttributeInLine(SuperInlineModelAdmin, admin.StackedInline):
    model = models.Attribute
    inlines = [AttributeValueInLine]


@admin.register(models.Category)
class CategoryAdmin(SuperModelAdmin):
    list_display = ('id', 'title', 'parent')
    list_display_links = (
        'id',
        'title',
    )
    search_fields = (
        'id',
        'title',
        'parent',
    )
    fields = ('title', 'parent', 'icon')
    inlines = [AttributeInLine]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'image',
        'short_description',
        'is_limited',
        'tags_display',
        'category',
        'created_at',
    )
    list_display_links = (
        'id',
        'title',
    )
    search_fields = (
        'id',
        'title',
    )
    fields = (
        'title',
        'image',
        'short_description',
        'long_description',
        'is_limited',
        'tags',
        'category',
        'created_at',
    )
    readonly_fields = (
        'rating',
        'created_at',
    )

    def tags_display(self, obj) -> str:
        return ", ".join([tag.title for tag in obj.tags.all()])

    tags_display.short_description = _('Tags')


@admin.register(models.DailyOffer)
class DailyOfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'select_date',
    )
    list_display_links = (
        'id',
        'product',
    )
    search_fields = (
        'id',
        'product',
        'select_date',
    )
    fields = (
        'product',
        'select_date',
    )


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'price',
        'count',
        'shop',
        'product',
    )
    list_display_links = (
        'id',
        'price',
    )
    search_fields = (
        'id',
        'price',
    )
    fields = (
        'price',
        'count',
        'shop',
        'product',
    )

