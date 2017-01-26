from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Employee
# Register your models here.
    
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee'
    list_fields = ["user","name","pos"]
    list_display = ["user","name","pos"]
    
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

