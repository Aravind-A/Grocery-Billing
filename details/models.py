from __future__ import unicode_literals

from django.db import models
from users.models import Employee

# Create your models here.

class Item(models.Model):

    item_name  = models.CharField(max_length = 100, default = 'Item Name')
    unit_price = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0.0)
    qty_avail  = models.IntegerField(default = 0)
    discount   = models.IntegerField(default = 0)

    class Meta:
        ordering = ('item_name',)
        
    def __unicode__(self):
        return str(self.id)
        
class Customer(models.Model):
    
    customer_name = models.CharField(max_length = 100, default = 'Customer Name')
    phone_number  = models.CharField(max_length = 15, default = 'Not Available')
    address       = models.TextField(default = 'Address')
    points        = models.DecimalField(max_digits = 7, decimal_places = 3, default = 0.0)
    
    class Meta:
        ordering = ('customer_name',)
        
    def __unicode__(self):
        return str(self.id)
        
class Bill(models.Model):
    
    bill_date  = models.DateField(auto_now = False, auto_now_add = True)
    bill_total = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.0)
    customer   = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
    cashier    = models.ForeignKey(Employee, on_delete = models.CASCADE, null = True)
    
    class Meta:
        ordering = ('bill_date',)
        
    def __unicode__(self):
        return str(self.id)
        
class Purchase(models.Model):
    
    bill          = models.ForeignKey(Bill, on_delete = models.CASCADE, null = True)
    item          = models.ForeignKey(Item, on_delete = models.CASCADE, null = True)
    qty_purchased = models.IntegerField(default = 0)
    
    class Meta:
        ordering = ('bill','item',)
        
    def __unicode__(self):
        return str(self.id)