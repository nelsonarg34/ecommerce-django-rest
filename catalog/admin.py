from atexit import register
from django.contrib import admin
from .models import Catalog, DayOfWeek


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', "type_of_catalog", "is_available", 'created', "updated",)

    search_fields = ("name", "type_of_catalog",)
    date_hierarchy = "created"
    list_editable = ['type_of_catalog', 'is_available',]
    prepopulated_fields = {'slug': ("name",)}

admin.site.register(DayOfWeek)