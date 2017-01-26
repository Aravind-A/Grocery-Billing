from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Employee(models.Model):
    
    POS_CHOICES = (('M','Manager'),('C','Cashier'))
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length = 50, default = 'Employee Name')
    pos  = models.CharField(max_length = 1, choices = POS_CHOICES)
    
    class Meta:
        ordering = ('-pos','name')
        
    def __unicode__(self):
        return self.user.username    