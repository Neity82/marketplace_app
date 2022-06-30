from modeltranslation.translator import register, TranslationOptions
from .models import Shop


@register(Shop)
class ShopTranslationOptions(TranslationOptions):
    fields = (
<<<<<<< HEAD
        "description",
        "address",
        "shipping_policy",
        "support_policy",
        "refund_policy",
        "quality_policy",
=======
        'name',
        'description',
        'address',
        'shipping_policy',
        'support_policy',
        'refund_policy',
        'quality_policy',
>>>>>>> 1797d9f1756005ab8f257a6239f444f0c0e947d6
    )
