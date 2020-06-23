from django.contrib import admin

# Register your models here.
from order import models


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'quantity', 'amount']
    list_filter = ['book']


# class DetailInline(admin.TabularInline):
#     model = models.OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name',
                    'phone', 'address', 'total', 'status')
    list_filter = ('status', 'create_at')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'zip_code',
                       'address', 'city', 'country', 'total', 'user')
    #inlines = [DetailInline]


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity',
                    'price', 'total', 'update_at')
    readonly_fields = ('book', 'quantity', 'price', 'total')


admin.site.register(models.ShopCart, ShopCartAdmin)
admin.site.register(models.OrderDetail, OrderDetailAdmin)
admin.site.register(models.Order, OrderAdmin)
