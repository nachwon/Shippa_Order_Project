from django.contrib import admin
from order.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'status',)
    fieldsets = (
        ("user_info", {'fields': ('user_id',)}),
        ("order_status", {'fields': ('status',)}),
        ("request message", {'fields': ('message',)}),
        ("merchant", {'fields': ('merchant_id',)})
    )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('menu_id', 'quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
