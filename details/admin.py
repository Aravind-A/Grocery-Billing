from django.contrib import admin
from .models import Item, Customer, Bill, Purchase
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ["id","item_name","unit_price","qty_avail","discount"]
    list_links = ["id"]
    
    class Meta:
        model = Item
        ordering = ("id",)
        
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id","customer_name","phone_number","address","points"]
    list_links = ["id"]
    
    class Meta:
        model = Customer
        ordering = ("id",)
        
class BillAdmin(admin.ModelAdmin):
    list_display = ["id","bill_date","bill_total","customer","cashier"]
    list_links = ["id","customer","cashier"]
    
    class Meta:
        model = Bill
        ordering = ("bill_date",)
        
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id","bill","item","qty_purchased"]
    list_links = ["id","bill","item"]
    
    class Meta:
        model = Purchase
        ordering = ("bill",)
        
admin.site.register(Item, ItemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Purchase, PurchaseAdmin)