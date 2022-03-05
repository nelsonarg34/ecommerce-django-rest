from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', "price", "stock", "is_available", 'created', "updated")

    search_fields = ("name", "category",)
    date_hierarchy = "created"
    list_editable = ['price', 'is_available', 'stock']
    prepopulated_fields = {'slug': ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "is_lux")
    list_editable = ['is_lux']
    prepopulated_fields = {'slug': ("name",)}
