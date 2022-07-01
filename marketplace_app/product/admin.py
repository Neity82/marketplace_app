from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

from modeltranslation.admin import TranslationAdmin

from product import models
from product.models import Product, Category
from product.utils import undelete_admin, DeletedFilter


class TranslationAdminMedia:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(models.Tag)
class TagAdmin(TranslationAdmin, TranslationAdminMedia):
    list_display = (
        'id',
        'title_en',
        'title_ru',
    )
    list_display_links = (
        'id',
        'title_en',
        'title_ru',
    )
    search_fields = (
        'id',
        'title_en',
        'title_ru',
    )
    fields = ('title',)


@admin.register(models.Attribute)
class AttributeAdmin(TranslationAdmin, TranslationAdminMedia):
    list_display = ('id', 'title_en', 'title_ru', 'category', 'type', 'help_text', 'rank',)
    list_display_links = ('id', 'title_en', 'title_ru', )
    search_fields = ('id', 'title_en', 'title_ru', 'category', 'help_text',)
    fields = ('title', 'type', 'category', 'help_text', 'rank',)
    list_filter = ('category', 'title_en', 'title_ru', 'rank')


@admin.register(models.Unit)
class UnitAdmin(TranslationAdmin, TranslationAdminMedia):
    list_display = ('title_en', 'title_ru', 'unit_description',)
    list_display_links = ('title_en', 'title_ru', 'unit_description',)
    search_fields = ('title_en', 'title_ru', 'unit_description',)
    fields = ('title', 'unit_description',)


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
class CategoryAdmin(TranslationAdmin, TranslationAdminMedia):
    change_form_template = "admin/undelete_change_form.html"
    list_display = (
        'id',
        'display_icon',
        'title_en',
        'title_ru',
        'parent',
        'sort_index',
    )
    list_display_links = (
        'id',
        'title_en',
        'title_ru',
    )
    search_fields = (
        'id',
        'title_en',
        'title_ru',
        'parent',
    )
    list_filter = (DeletedFilter, )
    fields = ('title', 'parent', 'icon', 'sort_index')

    @staticmethod
    def admin_manager():
        return Category.admin_objects

    # inlines = [AttributeInLine]

    @staticmethod
    def display_icon(obj):
        return mark_safe(f'<img src="{obj.icon.url}"  height="15" />')

    def response_change(self, request, obj):
        undelete_admin(self, request, obj)
        return super(CategoryAdmin, self).response_change(request, obj)


@admin.register(models.Product)
class ProductAdmin(TranslationAdmin, TranslationAdminMedia):
    change_form_template = "admin/undelete_change_form.html"
    list_display = (
        'id',
        'title_en',
        'title_ru',
        'image_display',
        'is_deleted',
        'short_description_en',
        'is_limited',
        'tags_display',
        'category',
        'created_at',
        'sort_index'
    )
    list_display_links = (
        'id',
        'title_en',
        'title_ru',
    )
    search_fields = (
        'id',
        'title_en',
        'title_ru',
    )
    fields = (
        'title',
        'image',
        'short_description',
        'long_description',
        'is_limited',
        'tags',
        'category',
        'rating',
        'created_at',
        'is_deleted',
    )

    list_filter = (
        'category',
        'is_limited',
        DeletedFilter,
    )

    readonly_fields = (
        'rating',
        'created_at',
        'is_deleted',
    )

    inlines = [AttributeValueInLine]

    @staticmethod
    def admin_manager():
        return Product.admin_objects

    @staticmethod
    def is_deleted(obj) -> bool:
        return obj.deleted_at is not None

    def tags_display(self, obj) -> str:
        return ", ".join([tag.title for tag in obj.tags.all()])

    def response_change(self, request, obj):
        attributes_by_category = models.Attribute.objects.filter(category=obj.category)
        for attribute in attributes_by_category:
            models.AttributeValue.objects.get_or_create(
                product=obj,
                attribute=attribute,
            )
        undelete_admin(self, request, obj)
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


@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'user',
        'product',
        'text',
        'rating'
    )
