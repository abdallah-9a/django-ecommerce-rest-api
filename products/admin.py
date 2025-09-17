from django.contrib import admin
from .models import Product, Category

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "stock"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
