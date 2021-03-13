from django.contrib import admin

from .models import Category, Product, Supplier, Supply, Bill


class BillAdmin(admin.ModelAdmin):
    list_display = ['supply', 'products_cost', 'discount', 'customer']


admin.site.register(Bill, BillAdmin)


class SupplyAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'supply_price', 'delivery_date', 'quantity']
admin.site.register(Supply,SupplyAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'agent', 'address', 'city', 'country', 'phone']


admin.site.register(Supplier,SupplierAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin,)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available'] # редактируем на странице отображения)
    prepopulated_fields = {'slug': ('name',)} #значение автоматом с использованием других полей


admin.site.register(Product, ProductAdmin)