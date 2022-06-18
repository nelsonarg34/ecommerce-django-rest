from atexit import register
from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'order',)

    search_fields = ("order",)
    date_hierarchy = "date_time"
    #list_editable = ['date_time',]
    #prepopulated_fields = {'slug': ("order",)}
