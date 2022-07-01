from modeltranslation.translator import register, TranslationOptions
from .models import Shop


@register(Shop)
class ShopTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
        "address",
        "shipping_policy",
        "support_policy",
        "refund_policy",
        "quality_policy",
    )
