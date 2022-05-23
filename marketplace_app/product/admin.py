from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# from modeltranslation.admin import TranslationAdmin
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
    fields = ('title',)


@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'help_text', 'rank',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'category', 'help_text',)
    fields = ('title', 'category', 'help_text', 'rank',)
    list_filter = ('category', 'title', 'rank')


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit', 'unit_description',)
    list_display_links = ('unit', 'unit_description',)
    search_fields = ('unit', 'unit_description',)
    fields = ('unit', 'unit_description',)


class ChildInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ChildInlineFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.order_by('-attribute__rank')


class AttributeValueInLine(admin.StackedInline):
    model = models.AttributeValue
    extra = 0
    formset = ChildInlineFormSet
    readonly_fields = ('attribute',)


@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value', 'unit',)
    list_display_links = ('product', 'attribute', 'value', 'unit',)
    search_fields = ('product', 'attribute', 'value', 'unit',)
    fields = ('product', 'attribute', 'value', 'unit',)
    # inlines = [AttributeInLine]


@admin.register(models.Category)
class CategoryAdmin(SuperModelAdmin):
    list_display = ('id', 'display_icon', 'title', 'parent', 'sort_index')
    list_display_links = (
        'id',
        'title',
    )
    search_fields = (
        'id',
        'title',
        'parent',
    )
    fields = ('title', 'parent', 'icon', 'sort_index')

    # inlines = [AttributeInLine]

    @staticmethod
    def display_icon(obj):
        return mark_safe(f'<img src="{obj.icon.url}"  height="15" />')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'image_display',
        'short_description',
        'is_limited',
        'tags_display',
        'category',
        'created_at',
        'sort_index'
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

    list_filter = (
        'category',
        'is_limited',
    )

    readonly_fields = (
        'rating',
        'created_at',
    )

    inlines = [AttributeValueInLine]

    def tags_display(self, obj) -> str:
        return ", ".join([tag.title for tag in obj.tags.all()])

    def response_change(self, request, obj):
        attributes_by_category = models.Attribute.objects.filter(category=obj.category)
        for attribute in attributes_by_category:
            models.AttributeValue.objects.get_or_create(
                product=obj,
                attribute=attribute,
            )
        return super(ProductAdmin, self).response_change(request, obj)

    @staticmethod
    def image_display(obj):
        return mark_safe(f'<img src="{obj.image.url}"  height="150" />')

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
    list_filter = (
        'shop',
        'product',
    )
