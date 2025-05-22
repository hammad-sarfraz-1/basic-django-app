from django.contrib import admin

# Register your models here.

from .models import Customer, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'joined_on')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'status', 'total_price')
    list_filter  = ('status', 'order_date')
    search_fields = ('customer__first_name', 'customer__last_name')
