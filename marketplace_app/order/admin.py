from django.contrib import admin

from order.models import Delivery, Order


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
