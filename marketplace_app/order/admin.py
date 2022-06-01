from django.contrib import admin

from order.models import Delivery, Order, OrderEntity, Cart


class OrderEntityInline(admin.StackedInline):
    model = OrderEntity
    extra = 1


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'datetime', 'user_id', 'state', 'error']
    inlines = [OrderEntityInline]


@admin.register(OrderEntity)
class OrderEntityAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'stock_id']
    list_display_links = ['id', 'order_id']
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # TODO stocks
    list_display = ['user_id', 'device', 'cart_entity_display', ]
    list_display_links = ['user_id', ]
    readonly_fields = ['device', ]

    @staticmethod
    def cart_entity_display(obj) -> str:
        return ", ".join([tag.title for tag in obj.cart_entity.all()])
