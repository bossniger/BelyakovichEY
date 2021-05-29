from django.contrib import admin

from apps.common.models import Country, City, Clients

admin.site.register(City)
admin.site.register(Country)


class ClientsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'amount_orders', 'orders_cost']


admin.site.register(Clients, ClientsAdmin)
# Register your models here.
