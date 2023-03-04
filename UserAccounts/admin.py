from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
# Register your models here.


# admin.site.register(CustomUser)
admin.site.register(otp)



class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'username', 'first_name',)
    # list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    ordering = ('-id',)
    list_display = ('id','username', 'user_type', 'first_name', 'last_name')
    fieldsets = (
        ('User Type', {'fields': ('user_type',)}),
        ("Details", {'fields': ('email', 'username', 'password', 'interests')}),
        
        ('Permissions', {'fields': ('is_active', 'is_staff', 'user_permissions')}),
        # ('Personal', {'fields': ('about',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_type', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
