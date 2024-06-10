from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category', 'in_stock')
    list_filter = ('name_category', 'in_stock',)
    search_fields = ('name_category', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_product', 'price', 'category')
    search_fields = ('name_product', 'description',)
