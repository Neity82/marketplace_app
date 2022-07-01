from modeltranslation.translator import register, TranslationOptions
from .models import SEOItem, Banner


@register(SEOItem)
class SEOTranslationOptions(TranslationOptions):
    fields = ("meta_title", "meta_description")


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ("title", "text", )
