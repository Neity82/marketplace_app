from modeltranslation.translator import register, TranslationOptions
from .models import Category, Tag, Unit, Attribute, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Unit)
class UnitTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Attribute)
class AttributeTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "short_description",
        "long_description",
    )
