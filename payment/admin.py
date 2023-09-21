from django.contrib import admin

from payment.models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "get_items")

    def name(self, obj):
        return obj

    def get_items(self, obj):
        return [item.name for item in obj.items.all()]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percent_off", "duration")


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("display_name", "inclusive", "percentage", "description")
