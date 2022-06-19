from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString
from django.utils.translation import gettext as _

from order import models


class OrderEntityInline(admin.StackedInline):
    model = models.OrderEntity
    extra = 1


@admin.register(models.DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "special_price",
        "cart_sum",
    )
    list_display_links = (
        "id",
        "name",
    )


@admin.register(models.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
        "address",
        "delivery_type",
    )
    list_display_links = (
        "id",
        "city",
    )

    @staticmethod
    def delivery_type(obj):
        delivery_type = getattr(obj, "delivery_type")
        return delivery_type.name if delivery_type else ""


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "datetime",
        "user_id",
        "state",
        "error",
    )
    inlines = [
        OrderEntityInline,
    ]


@admin.register(models.OrderEntity)
class OrderEntityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "stock_id",
    )
    list_display_links = (
        "id",
        "order_id",
    )


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user_display",
        "device",
        "cart_entity_display",
    )
    list_display_links = ("user_display",)
    readonly_fields = ("device",)

    @staticmethod
    def cart_entity_display(obj: models.Cart) -> SafeString:
        list_items = "".join(
            [
                f"<li>{cart_entity.stock.product.title}: {cart_entity.quantity} {_('pc')} </li>"
                for cart_entity in models.CartEntity.objects.filter(
                    cart=obj
                ).select_related("stock", "stock__product")
            ]
        )
        return mark_safe(f"<ul>{list_items}</ul>")

    @staticmethod
    def user_display(obj: models.Cart) -> str:
        result = "Unknown user"
        user = getattr(obj, "user_id", None)
        if user:
            user_name = user.__str__()
            if user_name:
                result = user_name
            else:
                result = getattr(user, "email")
        return result