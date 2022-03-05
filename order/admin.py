from django.contrib import admin
from .models import Order, OrderDetail

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id', "status", "is_paid", "buyer", "date_time")

    search_fields = ("status", "buyer")
    date_hierarchy = "date_time"
    list_editable = ["status"]


@admin.register(OrderDetail)
class OrerDetailAdmin(admin.ModelAdmin):

    list_display = ("order", "product", "quantity", "created", "updated")
    list_editable = ["quantity"]
    search_fields = ("order__status", "buyer", "product")
