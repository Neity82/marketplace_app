from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# from modeltranslation.admin import TranslationAdmin
from import_export.admin import ImportMixin
from import_export.forms import ConfirmImportForm
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from product import models
from product.forms import CustomImportForm
from product.resources import StockResource, ProductResource


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Представление модели Tag в интерфейсе администратора"""
    list_display = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
        "title",
    )
    search_fields = (
        "id",
        "title",
    )
    fields = ("title",)


@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    """Представление модели Attribute в интерфейсе администратора"""
    list_display = ("id", "title", "category", "type", "help_text", "rank",)
    list_display_links = ("id", "title",)
    search_fields = ("id", "title", "category", "help_text",)
    fields = ("title", "type", "category", "help_text", "rank",)
    list_filter = ("category", "title", "rank")


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    """Представление модели Unit в интерфейсе администратора"""
    list_display = ("unit", "unit_description",)
    list_display_links = ("unit", "unit_description",)
    search_fields = ("unit", "unit_description",)
    fields = ("unit", "unit_description",)


class ChildInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ChildInlineFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.order_by("-attribute__rank")


class AttributeValueInLine(admin.StackedInline):
    model = models.AttributeValue
    extra = 0
    formset = ChildInlineFormSet
    readonly_fields = ("attribute",)


@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    """Представление модели AttributeValue в интерфейсе администратора"""
    list_display = ("product", "attribute", "value", "unit",)
    list_display_links = ("product", "attribute", "value", "unit",)
    search_fields = ("product", "attribute", "value", "unit",)
    fields = ("product", "attribute", "value", "unit",)
    # inlines = [AttributeInLine]


@admin.register(models.Category)
class CategoryAdmin(SuperModelAdmin):
    """Представление модели Category в интерфейсе администратора"""
    list_display = ("id", "display_icon", "title", "parent", "sort_index")
    list_display_links = (
        "id",
        "title",
    )
    search_fields = (
        "id",
        "title",
        "parent",
    )
    fields = ("title", "parent", "icon", "sort_index")

    # inlines = [AttributeInLine]

    @staticmethod
    def display_icon(obj):
        return mark_safe(f'<img src="{obj.icon.url}"  height="15" />')


@admin.register(models.Product)
class ProductAdmin(ImportMixin, admin.ModelAdmin):
    """Представление модели Product в интерфейсе администратора"""
    list_display = (
        "id",
        "title",
        "image_display",
        "short_description",
        "is_limited",
        "tags_display",
        "category",
        "created_at",
        "sort_index"
    )
    list_display_links = (
        "id",
        "title",
    )
    search_fields = (
        "id",
        "title",
    )
    fields = (
        "title",
        "image",
        "short_description",
        "long_description",
        "is_limited",
        "tags",
        "category",
        "rating",
        "created_at",
    )

    list_filter = (
        "category",
        "is_limited",
    )

    readonly_fields = (
        "rating",
        "created_at",
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

    tags_display.short_description = _("Tags")

    resource_class = ProductResource


@admin.register(models.DailyOffer)
class DailyOfferAdmin(admin.ModelAdmin):
    """Представление модели DailyOffer в интерфейсе администратора"""
    list_display = (
        "id",
        "product",
        "select_date",
    )
    list_display_links = (
        "id",
        "product",
    )
    search_fields = (
        "id",
        "product",
        "select_date",
    )
    fields = (
        "product",
        "select_date",
    )


@admin.register(models.Stock)
class StockAdmin(ImportMixin, admin.ModelAdmin):
    """Представление модели Stock в интерфейсе администратора"""
    list_display = (
        "id",
        "price",
        "count",
        "shop",
        "product",
    )
    list_display_links = (
        "id",
        "price",
    )
    search_fields = (
        "id",
        "price",
    )
    fields = (
        "price",
        "count",
        "shop",
        "product",
    )
    list_filter = (
        "shop",
        "product",
    )

    resource_class = StockResource

    def get_import_form(self):
        return CustomImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance(form, CustomImportForm):
            if form.is_valid():
                shop = form.cleaned_data['shop']
                if shop:
                    kwargs.update({'shop': shop.id})

        return kwargs


@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Представление модели ProductReview в интерфейсе администратора"""
    list_display = (
        "date",
        "user",
        "product",
        "text",
        "rating"
    )
