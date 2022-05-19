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
    list_display = ['order_id', 'stock_id']
    list_display_links = ['order_id']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'stock_id', 'count']
    list_display_links = ['user_id']

